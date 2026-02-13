from django.contrib import admin
from ..models.ristoranti import Ristorante
from django.utils.translation import gettext_lazy as _

@admin.register(Ristorante)
class RistoranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'indirizzo', 'numeri')
    search_fields = ('nome', 'indirizzo')
    prepopulated_fields = {'slug': ('nome',)}
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('nome', 'slug')
        }),
        (_('Informazioni di Contatto'), {
            'fields': ('indirizzo', 'numeri')
        }),
        (_('Media'), {
            'fields': ('logo', 'menu')
        }),
    )
