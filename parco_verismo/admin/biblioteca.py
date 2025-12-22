"""
Admin per Opere e Autori.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Autore, Opera


@admin.register(Autore)
class AutoreAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)


@admin.register(Opera)
class OperaAdmin(TranslatableAdmin):
    list_display = ("__str__", "autore", "anno_pubblicazione")
    list_filter = ("autore",)
    search_fields = ("translations__titolo", "autore__nome")
    prepopulated_fields = {"slug": ("autore",)}
