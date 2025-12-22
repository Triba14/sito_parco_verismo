"""
Admin per Eventi e Notizie.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Evento, Notizia


@admin.register(Evento)
class EventoAdmin(TranslatableAdmin):
    list_display = ("__str__", "data_inizio", "data_fine", "is_active")
    list_filter = ("is_active", "data_inizio")
    search_fields = ("translations__titolo", "translations__luogo")
    date_hierarchy = "data_inizio"
    ordering = ("-data_inizio",)
    prepopulated_fields = {"slug": ("data_inizio",)}
    list_editable = ("is_active",)


@admin.register(Notizia)
class NotiziaAdmin(TranslatableAdmin):
    list_display = ("__str__", "data_pubblicazione", "is_active")
    list_filter = ("is_active", "data_pubblicazione")
    search_fields = ("translations__titolo", "translations__contenuto")
    date_hierarchy = "data_pubblicazione"
    ordering = ("-data_pubblicazione",)
    list_editable = ("is_active",)
