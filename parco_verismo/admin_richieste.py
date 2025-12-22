"""
Admin personalizzato per la gestione delle Richieste.
"""

# Standard library imports
from datetime import timedelta

# Django imports
from django.contrib import admin
from django.shortcuts import render
from django.urls import path

# Local imports
from .models import Richiesta


class RichiesteAdminSite(admin.AdminSite):
    """Admin site personalizzato per le richieste di contatto"""

    site_header = "Gestione Richieste di contatto - Parco Verismo"
    site_title = "Richieste di contatto"
    index_title = "Dashboard Richieste di contatto"

    def index(self, request, extra_context=None):
        """Reindirizza automaticamente alla dashboard personalizzata"""
        from django.shortcuts import redirect

        return redirect("richieste_admin:richieste_dashboard")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_view(self.dashboard_view),
                name="richieste_dashboard",
            ),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Vista dashboard semplificata per le richieste di contatto"""
        from django.utils import timezone

        oggi = timezone.now().date()
        settimana_fa = oggi - timedelta(days=7)

        # Statistiche essenziali
        stats = {
            "totali": Richiesta.objects.count(),
            "nuove": Richiesta.objects.filter(stato="nuova").count(),
            "in_lavorazione": Richiesta.objects.filter(
                stato="in_lavorazione"
            ).count(),
            "confermate": Richiesta.objects.filter(stato="confermata").count(),
            "completate": Richiesta.objects.filter(stato="completata").count(),
            "cancellate": Richiesta.objects.filter(stato="cancellata").count(),
            "priorita_alta": Richiesta.objects.filter(
                stato__in=["nuova", "in_lavorazione"], priorita="alta"
            ).count(),
            "settimana": Richiesta.objects.filter(
                data_richiesta__date__gte=settimana_fa
            ).count(),
        }

        # Richieste urgenti (priorità alta + non completate)
        richieste_urgenti = Richiesta.objects.filter(
            stato__in=["nuova", "in_lavorazione"], priorita="alta"
        ).order_by("-data_richiesta")[:10]

        # In ritardo: usa la property `in_ritardo` del modello (calcolo lato modello)
        in_ritardo = [
            p
            for p in Richiesta.objects.filter(
                stato__in=["nuova", "in_lavorazione", "confermata"]
            ).order_by("data_richiesta")
            if p.in_ritardo
        ][:10]

        # Ultime richieste attive
        richieste_recenti = Richiesta.objects.filter(
            stato__in=["nuova", "in_lavorazione", "confermata"]
        ).order_by("-data_richiesta")[:15]

        # Richieste cancellate
        richieste_cancellate = Richiesta.objects.filter(stato="cancellata").order_by(
            "-ultima_modifica"
        )[:15]

        context = {
            "stats": stats,
            "richieste_urgenti": richieste_urgenti,
            "in_ritardo": in_ritardo,
            "richieste_recenti": richieste_recenti,
            "richieste_cancellate": richieste_cancellate,
            "oggi": oggi,
        }

        return render(request, "admin/richieste_dashboard.html", context)


# Istanza del custom admin site
richieste_admin_site = RichiesteAdminSite(name="richieste_admin")


@admin.register(Richiesta, site=richieste_admin_site)
class RichiestaCustomAdmin(admin.ModelAdmin):
    """Admin semplificato per le richieste"""

    list_display = (
        "badge_stato",
        "nome_completo",
        "ente",
        "oggetto",
        "email_link",
        "priorita",
        "badge_ritardo",
        "guida_assegnata",
        "data_richiesta",
        "data_completamento",
    )
    list_filter = (
        "stato",
        "priorita",
        "data_richiesta",
    )
    search_fields = (
        "nome",
        "cognome",
        "email",
        "messaggio",
        "note_admin",
        "guida_assegnata",
        "ente",
        "oggetto",
    )
    date_hierarchy = "data_richiesta"
    ordering = ("-priorita", "-data_richiesta")
    list_editable = ("priorita",)
    readonly_fields = ("data_richiesta", "data_completamento", "ultima_modifica", "giorni_attesa_display")
    actions = [
        "cambia_stato_in_lavorazione",
        "cambia_stato_confermata",
        "cambia_stato_completata",
        "imposta_priorita_alta",
        "esporta_csv",
    ]

    fieldsets = (
        ("Informazioni contatto", {"fields": ("nome", "cognome", "email")}),
        (
            "Dettagli",
            {
                "fields": (
                    "messaggio",
                )
            },
        ),
        (
            "Gestione",
            {
                "fields": (
                    "stato",
                    "priorita",
                    "responsabile",
                    "guida_assegnata",
                    "note_admin",
                    "data_richiesta",
                    "data_completamento",
                    "ultima_modifica",
                    "giorni_attesa_display",
                ),
            },
        ),
    )
    list_per_page = 25

    def has_add_permission(self, request):
        """Disabilita la creazione - devono arrivare solo dal form pubblico"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disabilita la cancellazione per mantenere lo storico"""
        return False

    @admin.display(description="Nome", ordering="nome")
    def nome_completo(self, obj):
        return f"{obj.nome} {obj.cognome}"

    @admin.display(description="Email")
    def email_link(self, obj):
        from django.utils.html import format_html

        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    @admin.display(description="Stato")
    def badge_stato(self, obj):
        from django.utils.html import format_html

        colori_stato = {
            "nuova": "#17a2b8",
            "in_lavorazione": "#ffc107",
            "confermata": "#28a745",
            "completata": "#6c757d",
            "cancellata": "#dc3545",
        }
        color = colori_stato.get(obj.stato, "#6c757d")
        html = (
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-weight: 600; font-size: 11px; '
            'text-transform: uppercase;">{}</span>'
        )
        return format_html(html, color, obj.get_stato_display())

    @admin.display(description="Avviso")
    def badge_ritardo(self, obj):
        from django.utils.html import format_html

        if obj.in_ritardo:
            html = (
                '<span style="background: #dc3545; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: 600; font-size: 11px;">RITARDO</span>'
            )
            return format_html(html)
        return ""

    @admin.display(description="Tempo di gestione")
    def giorni_attesa_display(self, obj):
        giorni = obj.giorni_attesa
        return f"{giorni} giorni"

    @admin.action(description="In lavorazione")
    def cambia_stato_in_lavorazione(self, request, queryset):
        updated = queryset.update(
            stato="in_lavorazione", responsabile=request.user.username
        )
        self.message_user(request, f"{updated} richieste in lavorazione.")

    @admin.action(description="Conferma")
    def cambia_stato_confermata(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.stato = "confermata"
            obj.responsabile = request.user.username
            obj.save()
            count += 1
        self.message_user(request, f"{count} richieste confermate.", level="success")

    @admin.action(description="Completa")
    def cambia_stato_completata(self, request, queryset):
        from django.utils import timezone

        count = 0
        for obj in queryset:
            obj.stato = "completata"
            if not obj.data_completamento:
                obj.data_completamento = timezone.now()
            obj.responsabile = request.user.username
            obj.save()
            count += 1
        self.message_user(request, f"{count} richieste completate.", level="success")

    @admin.action(description="Priorità ALTA")
    def imposta_priorita_alta(self, request, queryset):
        updated = queryset.update(priorita="alta")
        self.message_user(
            request, f"{updated} richieste a priorità ALTA.", level="warning"
        )

    @admin.action(description="Esporta CSV")
    def esporta_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        filename = f"richieste_{timezone.now().strftime('%Y%m%d_%H%M')}.csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        response.write("\ufeff")  # BOM per Excel

        writer = csv.writer(response)
        writer.writerow(
            [
                "Nome",
                "Cognome",
                "Ente",
                "Oggetto",
                "Email",
                "Messaggio",
                "Stato",
                "Priorità",
                "Data richiesta",
                "Data completamento",
                "Responsabile",
                "Guida",
                "Note",
            ]
        )

        for obj in queryset:
            writer.writerow(
                [
                    obj.nome,
                    obj.cognome,
                    obj.ente or "",
                    obj.oggetto or "",
                    obj.email,
                    obj.messaggio,
                    obj.get_stato_display(),
                    obj.get_priorita_display(),
                    obj.data_richiesta.strftime("%d/%m/%Y %H:%M"),
                    obj.data_completamento.strftime("%d/%m/%Y %H:%M") if obj.data_completamento else "",
                    obj.responsabile or "",
                    obj.guida_assegnata or "",
                    obj.note_admin,
                ]
            )

        return response

    def changelist_view(self, request, extra_context=None):
        """Aggiungi statistiche alla vista lista"""
        extra_context = extra_context or {}
        extra_context["nuove"] = Richiesta.objects.filter(stato="nuova").count()
        extra_context["urgenti"] = Richiesta.objects.filter(
            stato__in=["nuova", "in_lavorazione"], priorita="alta"
        ).count()
        extra_context["in_ritardo"] = len(
            [
                p
                for p in Richiesta.objects.filter(
                    stato__in=["nuova", "in_lavorazione", "confermata"]
                )
                if p.in_ritardo
            ]
        )
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """Assegna automaticamente il responsabile"""
        if not obj.responsabile or "stato" in form.changed_data:
            obj.responsabile = request.user.username
        super().save_model(request, obj, form, change)
