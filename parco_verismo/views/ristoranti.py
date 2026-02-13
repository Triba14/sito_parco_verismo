from django.shortcuts import render
from ..models.ristoranti import Ristorante

def menu_del_verismo_view(request):
    """
    View per la pagina 'Menu del Verismo'.
    Recupera tutti i ristoranti dal database.
    """
    ristoranti = Ristorante.objects.all()
    return render(request, 'parco_verismo/menu_del_verismo.html', {
        'ristoranti': ristoranti,
    })
