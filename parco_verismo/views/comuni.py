"""
Views per i Comuni del Parco (Vizzini, Mineo, Licodia).
"""

# Django imports
from django.shortcuts import render


def licodia_view(request):
    """Pagina dedicata al comune di Licodia Eubea."""
    return render(request, "parco_verismo/licodia.html")


def mineo_view(request):
    """Pagina dedicata al comune di Mineo."""
    return render(request, "parco_verismo/mineo.html")


def vizzini_view(request):
    """Pagina dedicata al comune di Vizzini."""
    return render(request, "parco_verismo/vizzini.html")
