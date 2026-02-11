"""
Views per la Biblioteca e le Opere letterarie.
"""

# Django imports
from django.db.models import Q, Prefetch
from django.shortcuts import render, get_object_or_404
from collections import defaultdict

# Local imports
from ..models import Opera, Autore, LuogoLetterario, OperaInLuogo


def biblioteca_view(request):
    """Mostra tutte le opere e gestisce la ricerca per titolo e autore."""
    query = request.GET.get("q", "")
    opere_list = Opera.objects.all()

    if query:
        # Cerca nel titolo dell'opera O nel nome dell'autore
        opere_list = opere_list.filter(
            Q(translations__titolo__icontains=query) | Q(autore__nome__icontains=query)
        ).distinct()

    context = {
        "opere": opere_list,
        "query": query,
    }
    return render(request, "parco_verismo/biblioteca.html", context)


def opere_per_autore_view(request, autore_slug):
    """Pagina di presentazione delle opere di un singolo autore organizzate per luogo e categoria."""
    autore = get_object_or_404(Autore, slug=autore_slug)
    
    # Recupera tutte le relazioni OperaInLuogo per questo autore
    opere_in_luoghi = OperaInLuogo.objects.filter(
        opera__autore=autore
    ).select_related('opera', 'luogo').order_by('luogo__ordine', 'categoria', 'ordine')
    
    # Organizza le opere per luogo e categoria
    luoghi_dict = defaultdict(lambda: {
        'romanzi': [],
        'novelle': [],
        'teatro': [],
        'fiabe': []
    })
    
    for opera_in_luogo in opere_in_luoghi:
        luogo_nome = opera_in_luogo.luogo.nome
        categoria = opera_in_luogo.categoria
        luoghi_dict[luogo_nome][categoria].append(opera_in_luogo.opera)
    
    # Converti defaultdict in dict normale per il template
    luoghi_data = dict(luoghi_dict)
    
    context = {
        "autore": autore,
        "luoghi": luoghi_data,
    }
    return render(request, "parco_verismo/opere_per_autore.html", context)


def personaggi_lessico_view(request):
    """Pagina Personaggi e Lessico del Verismo."""
    return render(request, "parco_verismo/personaggi_lessico.html")


def luoghi_opere_view(request):
    """Pagina Luoghi delle Opere del Verismo."""
    return render(request, "parco_verismo/luoghi_opere.html")
