from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from ..models.ristoranti import Ristorante, LUOGO_CHOICES
from collections import defaultdict

def menu_del_verismo_view(request):
    """
    View per la pagina 'Menu del Verismo'.
    Recupera i ristoranti raggruppati per i tre luoghi principali.
    """
    codici_luoghi = [codice for codice, _ in LUOGO_CHOICES]
    ristoranti_list = Ristorante.objects.filter(
        luogo__in=codici_luoghi
    ).order_by('translations__nome').distinct()
    
    # Mappa codice → nome leggibile
    luogo_display = dict(LUOGO_CHOICES)
    
    # Raggruppa per luogo
    ristoranti_per_luogo = defaultdict(list)
    for r in ristoranti_list:
        nome_luogo = luogo_display.get(r.luogo, r.luogo)
        ristoranti_per_luogo[nome_luogo].append(r)
    
    # Costruisce la lista raggruppata seguendo l'ordine delle choices
    grouped_ristoranti = []
    for codice, nome in LUOGO_CHOICES:
        if ristoranti := ristoranti_per_luogo.get(nome):
            grouped_ristoranti.append((nome, ristoranti))

    return render(request, 'parco_verismo/menu_del_verismo.html', {
        'grouped_ristoranti': grouped_ristoranti,
        'ristoranti_count': ristoranti_list.count(),
    })
