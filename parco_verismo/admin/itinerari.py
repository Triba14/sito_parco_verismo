"""
Admin per Itinerari e Tappe.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Itinerario, TappaItinerario


@admin.register(Itinerario)
class ItinerarioAdmin(TranslatableAdmin):
    list_display = ("__str__", "tipo", "ordine", "difficolta", "is_active")
    list_filter = ("is_active", "tipo", "difficolta")
    search_fields = ("translations__titolo", "translations__descrizione")
    ordering = ("ordine", "translations__titolo")
    list_editable = ("ordine", "is_active")
    fieldsets = (
        (None, {"fields": ("slug", "tipo", "ordine", "is_active")}),
        ("Contenuto", {"fields": ("titolo", "descrizione", "immagine")}),
        (
            "Mappa Interattiva",
            {
                "fields": (
                    "coordinate_tappe",
                    "colore_percorso",
                    "icona_percorso",
                    "durata_stimata",
                    "difficolta",
                ),
                "description": "Configurazione per la mappa interattiva. coordinate_tappe deve essere un JSON valido.",
            },
        ),
        ("Link esterni", {"fields": ("link_maps",)}),
    )


@admin.register(TappaItinerario)
class TappaItinerarioAdmin(TranslatableAdmin):
    list_display = ("__str__", "itinerario", "ordine")
    list_filter = ("itinerario",)
    search_fields = ("translations__nome", "translations__descrizione")
    ordering = ("itinerario", "ordine")
    list_editable = ("ordine",)
