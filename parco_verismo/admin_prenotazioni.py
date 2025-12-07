"""
Admin personalizzato per la gestione delle Prenotazioni.
"""
# Standard library imports
from datetime import timedelta

# Django imports
from django.contrib import admin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

# Local imports
from .models import Prenotazione


class RichiesteAdminSite(admin.AdminSite):
    """Admin site personalizzato per le prenotazioni"""
    site_header = "Gestione Prenotazioni Parco Verismo"
    site_title = "Prenotazioni"
    index_title = "Dashboard Prenotazioni"
    
    def index(self, request, extra_context=None):
        """Reindirizza automaticamente alla dashboard personalizzata"""
        from django.shortcuts import redirect
        return redirect('richieste_admin:richieste_dashboard')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='richieste_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Vista dashboard semplificata per le prenotazioni"""
        oggi = timezone.now().date()
        settimana_fa = oggi - timedelta(days=7)
        
        # Statistiche essenziali
        stats = {
            'totali': Prenotazione.objects.count(),
            'nuove': Prenotazione.objects.filter(stato='nuova').count(),
            'in_lavorazione': Prenotazione.objects.filter(stato='in_lavorazione').count(),
            'confermate': Prenotazione.objects.filter(stato='confermata').count(),
            'completate': Prenotazione.objects.filter(stato='completata').count(),
            'cancellate': Prenotazione.objects.filter(stato='cancellata').count(),
            'priorita_alta': Prenotazione.objects.filter(
                stato__in=['nuova', 'in_lavorazione'],
                priorita='alta'
            ).count(),
            'settimana': Prenotazione.objects.filter(
                data_richiesta__date__gte=settimana_fa
            ).count(),
        }
        
        # Prenotazioni urgenti (priorità alta + non completate)
        richieste_urgenti = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione'],
            priorita='alta'
        ).order_by('-data_richiesta')[:10]
        
        # In ritardo (data preferita passata e non completate)
        in_ritardo = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione', 'confermata'],
            data_preferita__lt=oggi
        ).order_by('data_preferita')[:10]
        
        # Ultime prenotazioni attive
        richieste_recenti = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione', 'confermata']
        ).order_by('-data_richiesta')[:15]
        
        # Prenotazioni cancellate
        richieste_cancellate = Prenotazione.objects.filter(
            stato='cancellata'
        ).order_by('-ultima_modifica')[:15]
        
        # Distribuzione per luogo (attive)
        per_luogo = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione', 'confermata']
        ).values('luogo').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Distribuzione per itinerario (attive)
        per_itinerario = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione', 'confermata']
        ).values('itinerario').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context = {
            'stats': stats,
            'richieste_urgenti': richieste_urgenti,
            'in_ritardo': in_ritardo,
            'richieste_recenti': richieste_recenti,
            'richieste_cancellate': richieste_cancellate,
            'per_luogo': per_luogo,
            'per_itinerario': per_itinerario,
            'oggi': oggi,
        }
        
        return render(request, 'admin/prenotazioni_dashboard.html', context)


# Istanza del custom admin site
richieste_admin_site = RichiesteAdminSite(name='richieste_admin')


@admin.register(Prenotazione, site=richieste_admin_site)
class PrenotazioneCustomAdmin(admin.ModelAdmin):
    """Admin semplificato per le prenotazioni"""
    list_display = ('badge_stato', 'nome_completo', 'telefono', 'email_link', 'luogo', 'itinerario', 
                    'numero_partecipanti', 'data_preferita', 'priorita', 'badge_ritardo', 'guida_assegnata')
    list_filter = ('stato', 'priorita', 'luogo', 'itinerario', 'data_richiesta', 'data_preferita')
    search_fields = ('nome', 'cognome', 'email', 'telefono', 'messaggio', 'note_admin', 'guida_assegnata')
    date_hierarchy = 'data_richiesta'
    ordering = ('-priorita', '-data_richiesta')
    list_editable = ('priorita',)
    readonly_fields = ('data_richiesta', 'ultima_modifica', 'giorni_attesa_display')
    actions = ['cambia_stato_in_lavorazione', 'cambia_stato_confermata', 'cambia_stato_completata', 
               'imposta_priorita_alta', 'esporta_csv']
    list_per_page = 25
    
    def has_add_permission(self, request):
        """Disabilita la creazione - devono arrivare solo dal form pubblico"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disabilita la cancellazione per mantenere lo storico"""
        return False
    
    fieldsets = (
        ('Informazioni contatto', {
            'fields': ('nome', 'cognome', 'email', 'telefono')
        }),
        ('Dettagli richiesta', {
            'fields': ('luogo', 'itinerario', 'data_preferita', 'numero_partecipanti', 'messaggio')
        }),
        ('Gestione', {
            'fields': ('stato', 'priorita', 'responsabile', 'guida_assegnata', 'note_admin', 'data_richiesta', 'ultima_modifica', 'giorni_attesa_display'),
        }),
    )
    
    def nome_completo(self, obj):
        return f"{obj.nome} {obj.cognome}"
    nome_completo.short_description = "Nome"
    nome_completo.admin_order_field = 'nome'
    
    def email_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = "Email"
    
    def badge_stato(self, obj):
        from django.utils.html import format_html
        colori_stato = {
            'nuova': '#17a2b8',
            'in_lavorazione': '#ffc107',
            'confermata': '#28a745',
            'completata': '#6c757d',
            'cancellata': '#dc3545',
        }
        color = colori_stato.get(obj.stato, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: 600; font-size: 11px; text-transform: uppercase;">{}</span>',
            color, obj.get_stato_display()
        )
    badge_stato.short_description = "Stato"
    
    def badge_ritardo(self, obj):
        from django.utils.html import format_html
        if obj.in_ritardo:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: 600; font-size: 11px;">RITARDO</span>'
            )
        return ''
    badge_ritardo.short_description = "Avviso"
    
    def giorni_attesa_display(self, obj):
        giorni = obj.giorni_attesa
        return f"{giorni} giorni"
    giorni_attesa_display.short_description = "Tempo di gestione"
    
    def cambia_stato_in_lavorazione(self, request, queryset):
        updated = queryset.update(stato='in_lavorazione', responsabile=request.user.username)
        self.message_user(request, f"{updated} prenotazioni in lavorazione.")
    cambia_stato_in_lavorazione.short_description = "In lavorazione"
    
    def cambia_stato_confermata(self, request, queryset):
        from django.utils import timezone
        count = 0
        for obj in queryset:
            obj.stato = 'confermata'
            obj.responsabile = request.user.username
            obj.save()
            count += 1
        self.message_user(request, f"{count} prenotazioni confermate.", level='success')
    cambia_stato_confermata.short_description = "Conferma"
    
    def cambia_stato_completata(self, request, queryset):
        from django.utils import timezone
        count = 0
        for obj in queryset:
            obj.stato = 'completata'
            if not obj.data_completamento:
                obj.data_completamento = timezone.now()
            obj.responsabile = request.user.username
            obj.save()
            count += 1
        self.message_user(request, f"{count} prenotazioni completate.", level='success')
    cambia_stato_completata.short_description = "Completa"
    
    def imposta_priorita_alta(self, request, queryset):
        updated = queryset.update(priorita='alta')
        self.message_user(request, f"{updated} prenotazioni a priorità ALTA.", level='warning')
    imposta_priorita_alta.short_description = "Priorità ALTA"
    
    def esporta_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils import timezone
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="prenotazioni_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
        response.write('\ufeff')  # BOM per Excel
        
        writer = csv.writer(response)
        writer.writerow(['Nome', 'Cognome', 'Email', 'Telefono', 'Luogo', 'Itinerario', 
                        'Data preferita', 'N. Partecipanti', 'Messaggio', 'Stato', 'Priorità', 
                        'Data richiesta', 'Responsabile', 'Guida', 'Note'])
        
        for obj in queryset:
            writer.writerow([
                obj.nome, obj.cognome, obj.email, obj.telefono, obj.get_luogo_display(),
                obj.get_itinerario_display(), obj.data_preferita or '', obj.numero_partecipanti,
                obj.messaggio, obj.get_stato_display(), obj.get_priorita_display(),
                obj.data_richiesta.strftime('%d/%m/%Y %H:%M'), obj.responsabile or '', 
                obj.guida_assegnata or '', obj.note_admin
            ])
        
        return response
    esporta_csv.short_description = "Esporta CSV"
    
    def changelist_view(self, request, extra_context=None):
        """Aggiungi statistiche alla vista lista"""
        extra_context = extra_context or {}
        extra_context['nuove'] = Prenotazione.objects.filter(stato='nuova').count()
        extra_context['urgenti'] = Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione'],
            priorita='alta'
        ).count()
        extra_context['in_ritardo'] = len([p for p in Prenotazione.objects.filter(
            stato__in=['nuova', 'in_lavorazione', 'confermata']
        ) if p.in_ritardo])
        return super().changelist_view(request, extra_context=extra_context)
    
    def save_model(self, request, obj, form, change):
        """Assegna automaticamente il responsabile"""
        if not obj.responsabile or 'stato' in form.changed_data:
            obj.responsabile = request.user.username
        super().save_model(request, obj, form, change)
