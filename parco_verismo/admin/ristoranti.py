from django.contrib import admin
from ..models.ristoranti import Ristorante
from django.utils.translation import gettext_lazy as _

@admin.register(Ristorante)
class RistoranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'luogo', 'indirizzo', 'numeri')
    search_fields = ('nome', 'indirizzo')
    readonly_fields = ('slug',)
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('nome', 'tipo', 'luogo')
        }),
        (_('Informazioni di Contatto'), {
            'fields': ('indirizzo', 'numeri', 'link_maps')
        }),
        (_('Media'), {
            'fields': ('logo', 'menu')
        }),
    )
