"""
Views per Eventi, Notizie e Calendario.
"""

# Django imports
from django.shortcuts import render, get_object_or_404
from django.utils import timezone, translation

# Local imports
from ..models import Evento, Notizia


def eventi_view(request):
    """Mostra tutti gli eventi attivi ordinati per data con notizie."""
    eventi = Evento.objects.filter(
        is_active=True, data_inizio__gte=timezone.now()
    ).order_by("data_inizio")
    notizie = Notizia.objects.filter(is_active=True).order_by("-data_pubblicazione")[
        :20
    ]
    context = {
        "eventi": eventi,
        "notizie": notizie,
    }
    return render(request, "parco_verismo/eventi.html", context)


def calendario_view(request):
    """Mostra il calendario degli eventi."""
    eventi = Evento.objects.filter(is_active=True).order_by("data_inizio")
    context = {
        "eventi": eventi,
        "LANGUAGE_CODE": translation.get_language(),
    }
    return render(request, "parco_verismo/calendario.html", context)


def evento_detail_view(request, slug):
    """Pagina di dettaglio di un singolo evento."""
    evento = get_object_or_404(Evento, slug=slug, is_active=True)
    context = {
        "evento": evento,
    }
    return render(request, "parco_verismo/evento_detail.html", context)


def notizie_view(request):
    """Mostra tutte le notizie attive ordinate per data di pubblicazione."""
    notizie = Notizia.objects.filter(is_active=True).order_by("-data_pubblicazione")
    eventi = Evento.objects.filter(
        is_active=True, data_inizio__gte=timezone.now()
    ).order_by("data_inizio")[:20]
    context = {
        "notizie": notizie,
        "eventi": eventi,
    }
    return render(request, "parco_verismo/notizie.html", context)


def notizia_detail_view(request, slug):
    """Pagina di dettaglio di una singola notizia."""
    notizia = get_object_or_404(Notizia, slug=slug, is_active=True)
    context = {
        "notizia": notizia,
    }
    return render(request, "parco_verismo/notizia_detail.html", context)
