"""
Admin per Richieste.
"""

# Django imports
from django.contrib import admin

# Local imports
from ..models import Richiesta


@admin.register(Richiesta)
class RichiestaAdmin(admin.ModelAdmin):
    """Admin di base per le richieste nel pannello principale."""

    list_display = (
        "badge_stato",
        "nome_completo",
        "ente",
        "oggetto",
        "email_link",
        "priorita",
        "data_richiesta",
        "data_completamento",
        "responsabile",
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
        "ente",
        "oggetto",
    )
    date_hierarchy = "data_richiesta"
    ordering = ("-priorita", "-data_richiesta")
    list_editable = ("priorita",)
    readonly_fields = ("data_richiesta", "data_completamento", "ultima_modifica")
    actions = [
        "marca_come_confermata",
        "marca_come_completata",
        "imposta_priorita_alta",
        "esporta_csv",
    ]

    fieldsets = (
        (
            "Informazioni contatto",
            {"fields": ("nome", "cognome", "email", "ente", "oggetto")},
        ),
        (
            "Dettagli richiesta",
            {
                "fields": (
                    "messaggio",
                )
            },
        ),
        (
            "Gestione amministrativa",
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
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        """Reindirizza alla dashboard personalizzata invece della lista standard."""
        from django.shortcuts import redirect

        return redirect("/richieste/")

    def has_add_permission(self, request):
        """Disabilita la creazione di richieste dall'admin - devono arrivare solo dal form pubblico."""
        return False

    @admin.display(description="Nome completo", ordering="nome")
    def nome_completo(self, obj):
        return f"{obj.nome} {obj.cognome}"

    @admin.display(description="Email", ordering="email")
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

    @admin.action(description="Marca come confermata")
    def marca_come_confermata(self, request, queryset):
        updated = queryset.update(
            stato="confermata", responsabile=request.user.username
        )
        self.message_user(
            request, f"{updated} richieste confermate.", level="success"
        )

    @admin.action(description="Marca come completata")
    def marca_come_completata(self, request, queryset):
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

    @admin.action(description="Imposta priorità ALTA")
    def imposta_priorita_alta(self, request, queryset):
        updated = queryset.update(priorita="alta")
        self.message_user(
            request,
            f"{updated} richieste impostate a priorità alta.",
            level="warning",
        )

    def esporta_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="richieste_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
        )
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
                ]
            )

        return response
