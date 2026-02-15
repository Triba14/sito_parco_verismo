from django.contrib import admin
from parler.admin import TranslatableAdmin
from ..models.ristoranti import Ristorante
from django.utils.translation import gettext_lazy as _

@admin.register(Ristorante)
class RistoranteAdmin(TranslatableAdmin):
    list_display = ('nome', 'luogo', 'indirizzo', 'numeri')
    search_fields = ('translations__nome', 'translations__indirizzo')
    readonly_fields = ('slug',)
    list_per_page = 20
