"""
Admin per Documenti e Archivio Fotografico.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Documento, FotoArchivio


@admin.register(Documento)
class DocumentoAdmin(TranslatableAdmin):
    list_display = (
        "__str__",
        "tipo",
        "autori",
        "anno_pubblicazione",
        "data_pubblicazione",
        "is_active",
    )
    list_filter = ("is_active", "tipo", "anno_pubblicazione", "data_pubblicazione")
    search_fields = ("translations__titolo", "translations__descrizione", "autori")
    date_hierarchy = "data_pubblicazione"
    ordering = ("-data_pubblicazione",)
    list_editable = ("is_active",)
    fieldsets = (
        (None, {"fields": ("slug", "tipo", "is_active")}),
        (
            "Contenuto",
            {"fields": ("titolo", "descrizione", "riassunto", "parole_chiave")},
        ),
        ("File e Media", {"fields": ("pdf_file", "anteprima")}),
        ("Informazioni", {"fields": ("autori", "anno_pubblicazione")}),
    )


@admin.register(FotoArchivio)
class FotoArchivioAdmin(TranslatableAdmin):
    list_display = (
        "__str__",
        "autore",
        "categoria",
        "ordine",
        "data_aggiunta",
        "is_active",
    )
    list_filter = ("is_active", "autore", "categoria", "data_aggiunta")
    search_fields = ("translations__titolo", "translations__descrizione", "categoria")
    date_hierarchy = "data_aggiunta"
    ordering = ("ordine", "-data_aggiunta")
    list_editable = ("ordine", "is_active")
    fieldsets = (
        (None, {"fields": ("immagine", "autore", "categoria", "ordine", "is_active")}),
        ("Informazioni", {"fields": ("titolo", "descrizione")}),
    )
