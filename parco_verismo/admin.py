# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin, TranslatableTabularInline

# Local imports
from .models import (
    Autore, Opera, Evento, Notizia, Documento, 
    FotoArchivio, Itinerario, TappaItinerario, Prenotazione
)

@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)


@admin.register(Opera)
class OperaAdmin(TranslatableAdmin):
    list_display = ('__str__', 'autore', 'anno_pubblicazione')
    list_filter = ('autore',)
    search_fields = ('translations__titolo', 'autore__nome')
    prepopulated_fields = {'slug': ('autore',)}


@admin.register(Evento)
class EventoAdmin(TranslatableAdmin):
    list_display = ('__str__', 'data_inizio', 'data_fine', 'is_active')
    list_filter = ('is_active', 'data_inizio')
    search_fields = ('translations__titolo', 'translations__luogo')
    date_hierarchy = 'data_inizio'
    ordering = ('-data_inizio',)
    prepopulated_fields = {'slug': ('data_inizio',)}
    list_editable = ('is_active',)


@admin.register(Notizia)
class NotiziaAdmin(TranslatableAdmin):
    list_display = ('__str__', 'data_pubblicazione', 'is_active')
    list_filter = ('is_active', 'data_pubblicazione')
    search_fields = ('translations__titolo', 'translations__contenuto')
    date_hierarchy = 'data_pubblicazione'
    ordering = ('-data_pubblicazione',)
    list_editable = ('is_active',)


@admin.register(Documento)
class DocumentoAdmin(TranslatableAdmin):
    list_display = ('__str__', 'tipo', 'autori', 'anno_pubblicazione', 'data_pubblicazione', 'is_active')
    list_filter = ('is_active', 'tipo', 'anno_pubblicazione', 'data_pubblicazione')
    search_fields = ('translations__titolo', 'translations__descrizione', 'autori')
    date_hierarchy = 'data_pubblicazione'
    ordering = ('-data_pubblicazione',)
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('slug', 'tipo', 'is_active')
        }),
        ('Contenuto', {
            'fields': ('titolo', 'descrizione', 'riassunto', 'parole_chiave')
        }),
        ('File e Media', {
            'fields': ('pdf_file', 'anteprima')
        }),
        ('Informazioni', {
            'fields': ('autori', 'anno_pubblicazione')
        }),
    )


@admin.register(FotoArchivio)
class FotoArchivioAdmin(TranslatableAdmin):
    list_display = ('__str__', 'categoria', 'ordine', 'data_aggiunta', 'is_active')
    list_filter = ('is_active', 'categoria', 'data_aggiunta')
    search_fields = ('translations__titolo', 'translations__descrizione', 'categoria')
    date_hierarchy = 'data_aggiunta'
    ordering = ('ordine', '-data_aggiunta')
    list_editable = ('ordine', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('immagine', 'categoria', 'ordine', 'is_active')
        }),
        ('Informazioni', {
            'fields': ('titolo', 'descrizione')
        }),
    )


@admin.register(Itinerario)
class ItinerarioAdmin(TranslatableAdmin):
    list_display = ('__str__', 'tipo', 'ordine', 'difficolta', 'is_active')
    list_filter = ('is_active', 'tipo', 'difficolta')
    search_fields = ('translations__titolo', 'translations__descrizione')
    ordering = ('ordine', 'translations__titolo')
    list_editable = ('ordine', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('slug', 'tipo', 'ordine', 'is_active')
        }),
        ('Contenuto', {
            'fields': ('titolo', 'descrizione', 'immagine')
        }),
        ('Mappa Interattiva', {
            'fields': ('coordinate_tappe', 'colore_percorso', 'icona_percorso', 'durata_stimata', 'difficolta'),
            'description': 'Configurazione per la mappa interattiva. coordinate_tappe deve essere un JSON valido.'
        }),
        ('Link esterni', {
            'fields': ('link_maps',)
        }),
    )


@admin.register(TappaItinerario)
class TappaItinerarioAdmin(TranslatableAdmin):
    list_display = ('__str__', 'itinerario', 'ordine')
    list_filter = ('itinerario',)
    search_fields = ('translations__nome', 'translations__descrizione')
    ordering = ('itinerario', 'ordine')
    list_editable = ('ordine',)


@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    """Admin di base per le prenotazioni nel pannello principale."""
    list_display = ('badge_stato', 'nome_completo', 'telefono', 'email_link', 'luogo', 'itinerario', 
                    'numero_partecipanti', 'data_preferita', 'priorita', 'data_richiesta', 'responsabile')
    list_filter = ('stato', 'priorita', 'luogo', 'itinerario', 'data_richiesta', 'data_preferita', 'numero_partecipanti')
    search_fields = ('nome', 'cognome', 'email', 'telefono', 'messaggio')
    date_hierarchy = 'data_richiesta'
    ordering = ('-priorita', '-data_richiesta')
    list_editable = ('priorita',)
    readonly_fields = ('data_richiesta', 'ultima_modifica')
    actions = ['marca_come_confermata', 'marca_come_completata', 'imposta_priorita_alta', 'esporta_csv']
    
    def changelist_view(self, request, extra_context=None):
        """Reindirizza alla dashboard personalizzata invece della lista standard."""
        from django.shortcuts import redirect
        return redirect('/richieste/')
    
    def has_add_permission(self, request):
        """Disabilita la creazione di richieste dall'admin - devono arrivare solo dal form pubblico."""
        return False
    
    fieldsets = (
        ('Informazioni contatto', {
            'fields': ('nome', 'cognome', 'email', 'telefono')
        }),
        ('Dettagli richiesta', {
            'fields': ('luogo', 'itinerario', 'data_preferita', 'numero_partecipanti', 'messaggio')
        }),
        ('Gestione amministrativa', {
            'fields': ('stato', 'priorita', 'responsabile', 'guida_assegnata', 'note_admin', 'data_richiesta', 'ultima_modifica'),
            'classes': ('collapse',)
        }),
    )
    
    def nome_completo(self, obj):
        return f"{obj.nome} {obj.cognome}"
    nome_completo.short_description = "Nome completo"
    nome_completo.admin_order_field = 'nome'
    
    def email_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = "Email"
    email_link.admin_order_field = 'email'
    
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
    
    def marca_come_confermata(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(stato='confermata', responsabile=request.user.username)
        self.message_user(request, f"{updated} prenotazioni confermate.", level='success')
    marca_come_confermata.short_description = "Marca come confermata"
    
    def marca_come_completata(self, request, queryset):
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
    marca_come_completata.short_description = "Marca come completata"
    
    def imposta_priorita_alta(self, request, queryset):
        updated = queryset.update(priorita='alta')
        self.message_user(request, f"{updated} prenotazioni impostate a priorità alta.", level='warning')
    imposta_priorita_alta.short_description = "Imposta priorità ALTA"
    
    def esporta_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils import timezone
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="richieste_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
        response.write('\ufeff')  # BOM per Excel
        
        writer = csv.writer(response)
        writer.writerow(['Nome', 'Cognome', 'Email', 'Telefono', 'Luogo', 'Itinerario', 
                        'Data preferita', 'N. Partecipanti', 'Messaggio', 'Stato', 'Priorità', 
                        'Data richiesta', 'Responsabile'])
        
        for obj in queryset:
            writer.writerow([
                obj.nome, obj.cognome, obj.email, obj.telefono, obj.get_luogo_display(),
                obj.get_itinerario_display(), obj.data_preferita or '', obj.numero_partecipanti,
                obj.messaggio, obj.get_stato_display(), obj.get_priorita_display(),
                obj.data_richiesta.strftime('%d/%m/%Y %H:%M'), obj.responsabile or ''
            ])
        
        return response
    esporta_csv.short_description = "Esporta in CSV"


