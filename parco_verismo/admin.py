from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Autore, Opera, Evento, Notizia, Documento, FotoArchivio

@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Opera)
class OperaAdmin(TranslatableAdmin):
    list_display = ('__str__', 'autore', 'anno_pubblicazione')
    list_filter = ('autore',)
    search_fields = ('translations__titolo', 'autore__nome')

@admin.register(Evento)
class EventoAdmin(TranslatableAdmin):
    list_display = ('__str__', 'data_inizio', 'is_active')
    list_filter = ('is_active', 'data_inizio')
    search_fields = ('translations__titolo', 'translations__luogo')
    date_hierarchy = 'data_inizio'
    ordering = ('-data_inizio',)

@admin.register(Notizia)
class NotiziaAdmin(TranslatableAdmin):
    list_display = ('__str__', 'data_pubblicazione', 'is_active')
    list_filter = ('is_active', 'data_pubblicazione')
    search_fields = ('translations__titolo', 'translations__contenuto')
    date_hierarchy = 'data_pubblicazione'
    ordering = ('-data_pubblicazione',)

@admin.register(Documento)
class DocumentoAdmin(TranslatableAdmin):
    list_display = ('__str__', 'tipo', 'autori', 'anno_pubblicazione', 'data_pubblicazione', 'is_active')
    list_filter = ('is_active', 'tipo', 'anno_pubblicazione', 'data_pubblicazione')
    search_fields = ('translations__titolo', 'translations__descrizione', 'autori')
    date_hierarchy = 'data_pubblicazione'
    ordering = ('-data_pubblicazione',)
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
