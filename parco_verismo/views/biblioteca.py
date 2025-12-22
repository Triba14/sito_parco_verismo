"""
Views per la Biblioteca e le Opere letterarie.
"""

# Django imports
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Local imports
from ..models import Opera, Autore


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
    """Pagina di presentazione delle opere di un singolo autore."""
    autore = get_object_or_404(Autore, slug=autore_slug)
    opere_autore = Opera.objects.filter(autore=autore)
    context = {
        "autore": autore,
        "opere": opere_autore,
    }
    return render(request, "parco_verismo/opere_per_autore.html", context)


def opera_detail_view(request, slug):
    """Pagina di dettaglio della singola opera con trama e analisi."""
    opera = get_object_or_404(Opera, slug=slug)
    context = {
        "opera": opera,
    }
    return render(request, "parco_verismo/opera_detail.html", context)


def personaggi_lessico_view(request):
    """Pagina Personaggi e Lessico del Verismo."""
    return render(request, "parco_verismo/personaggi_lessico.html")


def luoghi_opere_view(request):
    """Pagina Luoghi delle Opere del Verismo."""
    return render(request, "parco_verismo/luoghi_opere.html")
