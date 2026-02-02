"""
Admin per Itinerari - Sistema Rinnovato
"""

# Django imports
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
import json

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Itinerario, ItinerarioImmagine


class ItinerarioImmagineInline(admin.TabularInline):
    """
    Inline per caricare multiple immagini nella galleria dell'itinerario.
    """
    model = ItinerarioImmagine
    extra = 1
    fields = ('immagine', 'ordine', 'didascalia')
    verbose_name = "Immagine Galleria"
    verbose_name_plural = "📸 Galleria Immagini (Carosello)"


@admin.register(Itinerario)
class ItinerarioAdmin(TranslatableAdmin):
    """
    Amministrazione per gli itinerari letterari con supporto completo per mappe interattive.
    """
    
    inlines = [ItinerarioImmagineInline]
    
    list_display = (
        'itinerario_icon',
        'titolo_breve', 
        'tipo', 
        'ordine', 
        'numero_tappe',
        'durata_stimata', 
        'difficolta', 
        'is_active',
        'azioni_rapide'
    )
    
    list_filter = ('tipo', 'difficolta', 'is_active', 'created_at')
    search_fields = ('translations__titolo', 'translations__descrizione', 'slug')
    ordering = ('tipo', 'ordine')
    list_editable = ('ordine', 'is_active')
    
    readonly_fields = ('created_at', 'updated_at', 'anteprima_mappa')
    
    fieldsets = (
        ('📋 Informazioni Base', {
            'fields': ('titolo', 'slug', 'tipo', 'ordine', 'is_active')
        }),
        ('📝 Descrizione', {
            'fields': ('descrizione', 'note')
        }),
        ('🖼️ Media', {
            'fields': ('immagine',),
            'description': 'Immagine di copertina dell\'itinerario. La galleria per il carosello si gestisce nella sezione "Galleria Immagini" sotto.'
        }),
        ('🗺️ Dettagli Percorso', {
            'fields': ('durata_stimata', 'difficolta', 'colore_percorso'),
            'description': 'Informazioni sul percorso e visualizzazione sulla mappa'
        }),
        ('📍 Coordinate e Tappe', {
            'fields': ('coordinate_tappe', 'anteprima_mappa'),
            'description': mark_safe(
                '<p><strong>Formato JSON per le tappe:</strong></p>'
                '<pre style="background: #f5f5f5; padding: 10px; border-radius: 4px;">'
                '[\n'
                '  {\n'
                '    "nome": "Chiesa del Crocifisso",\n'
                '    "coords": [37.157833, 14.704139],\n'
                '    "descrizione_breve": "Breve descrizione per il popup del marker",\n'
                '    "descrizione": "Descrizione completa e dettagliata per il modale.\\n\\nPuoi usare più paragrafi separati da \\\\n\\\\n",\n'
                '    "immagine": "/static/media/itinerari/chiesa_crocifisso.jpg",\n'
                '    "order": 1,\n'
                '    "tratteggiato": false\n'
                '  },\n'
                '  {\n'
                '    "nome": "Piazza Garibaldi",\n'
                '    "coords": [37.158556, 14.703722],\n'
                '    "descrizione_breve": "Antica piazza principale",\n'
                '    "descrizione": "Storia completa della piazza con dettagli architettonici e aneddoti",\n'
                '    "order": 2,\n'
                '    "tratteggiato": false\n'
                '  }\n'
                ']'
                '</pre>'
                '<p><strong>Nota:</strong></p>'
                '<ul>'
                '<li><code>descrizione_breve</code>: Testo breve (1-2 righe) mostrato nel popup del marker</li>'
                '<li><code>descrizione</code>: Testo completo mostrato nel modale informazioni</li>'
                '<li><code>immagine</code>: (OPZIONALE) Path relativo all\'immagine della tappa. Se non specificata, viene mostrato il logo del Parco</li>'
                '<li><code>tratteggiato</code>: true se il percorso verso la prossima tappa è tratteggiato (non percorribile)</li>'
                '</ul>'
            )
        }),
        ('🔗 Link Esterni', {
            'fields': ('link_maps',),
            'classes': ('collapse',)
        }),
        ('⏰ Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Ottimizza le query con prefetch"""
        return super().get_queryset(request).prefetch_related('translations')
    
    @admin.display(description='')
    def itinerario_icon(self, obj):
        """Mostra l'icona dell'itinerario"""
        return format_html(
            '<span style="font-size: 24px;">{}</span>',
            '📍'
        )
    
    @admin.display(description='Titolo', ordering='translations__titolo')
    def titolo_breve(self, obj):
        """Mostra il titolo con il tipo"""
        titolo = obj.titolo if hasattr(obj, 'titolo') else 'Senza titolo'
        tipo_badge_colors = {
            'verghiano': '#8B4513',
            'capuaniano': '#2E7D32',
            'tematico': '#1976D2'
        }
        color = tipo_badge_colors.get(obj.tipo, '#666')
        
        return format_html(
            '<strong>{}</strong>',
            titolo[:50] + '...' if len(titolo) > 50 else titolo
        )
    
    @admin.display(description='Tappe')
    def numero_tappe(self, obj):
        """Mostra il numero di tappe"""
        num = obj.get_numero_tappe()
        if num == 0:
            return format_html('<span style="color: #999;">Nessuna</span>')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.colore_percorso,
            num
        )
    
    @admin.display(description='Azioni')
    def azioni_rapide(self, obj):
        """Mostra link rapidi"""
        url = obj.get_absolute_url()
        return format_html(
            '<a href="{}" target="_blank" style="color: #0066cc;">🔗 Vedi sul sito</a>',
            url
        )
    
    @admin.display(description='Anteprima Mappa')
    def anteprima_mappa(self, obj):
        """Mostra un'anteprima delle coordinate"""
        if not obj.coordinate_tappe:
            return format_html('<em style="color: #999;">Nessuna coordinata definita</em>')
        
        try:
            if isinstance(obj.coordinate_tappe, str):
                tappe = json.loads(obj.coordinate_tappe)
            else:
                tappe = obj.coordinate_tappe
            
            html = '<div style="background: #f9f9f9; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">'
            html += f'<p><strong>📍 Totale tappe:</strong> {len(tappe)}</p>'
            html += '<ul style="margin: 10px 0; padding-left: 20px;">'
            
            for tappa in sorted(tappe, key=lambda x: x.get('order', 0))[:5]:
                nome = tappa.get('nome', 'Senza nome')
                coords = tappa.get('coords', [])
                order = tappa.get('order', '?')
                if coords and len(coords) >= 2:
                    html += f'<li><strong>{order}.</strong> {nome} <code style="background: #e8e8e8; padding: 2px 5px; border-radius: 3px; font-size: 11px;">({coords[0]:.6f}, {coords[1]:.6f})</code></li>'
            
            if len(tappe) > 5:
                html += f'<li><em>... e altre {len(tappe) - 5} tappe</em></li>'
            
            html += '</ul>'
            html += f'<p><strong>🎯 Centro mappa:</strong> <code style="background: #e8e8e8; padding: 2px 5px; border-radius: 3px;">{obj.get_centro_mappa()}</code></p>'
            html += '</div>'
            
            return format_html(html)
        except Exception as e:
            return format_html('<p style="color: red;">⚠️ Errore nel parsing del JSON: {}</p>', str(e))
    
    class Media:
        css = {
            'all': ('admin/css/itinerari-admin.css',)
        }
        js = ('admin/js/itinerari-admin.js',)

