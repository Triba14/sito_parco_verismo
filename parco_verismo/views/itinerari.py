"""
Views per Itinerari turistici.
"""

# Standard library imports
import json

# Django imports
from django.shortcuts import render, get_object_or_404

# Local imports
from ..models import Itinerario


def itinerari_verghiani_view(request):
    """Lista degli itinerari di tipo 'verghiano'."""
    itinerari = Itinerario.objects.filter(is_active=True, tipo="verghiano").order_by(
        "ordine", "translations__titolo"
    )

    # Prepara i dati per il template con serializzazione corretta
    itinerari_data = []
    for itinerario in itinerari:
        coordinate_tappe = (
            itinerario.coordinate_tappe if itinerario.coordinate_tappe else []
        )
        # Serializza l'intero oggetto itinerario per evitare problemi di escaping
        itinerario_json = json.dumps(
            {
                "slug": itinerario.slug,
                "titolo": itinerario.titolo,
                "descrizione_breve": (
                    " ".join(itinerario.descrizione.split()[:15]) + "..."
                    if itinerario.descrizione
                    else ""
                ),
                "colore": itinerario.colore_percorso or "#2E7D32",
                "icona": itinerario.icona_percorso or "📖",
                "durata": itinerario.durata_stimata or "",
                "difficolta": (
                    itinerario.get_difficolta_display() if itinerario.difficolta else ""
                ),
                "coordinate_tappe": coordinate_tappe,
            },
            ensure_ascii=False,
        )
        itinerari_data.append({"obj": itinerario, "itinerario_json": itinerario_json})

    context = {"itinerari": itinerari, "itinerari_data": itinerari_data}
    return render(request, "parco_verismo/itinerari_verghiani.html", context)


def itinerari_capuaniani_view(request):
    """Lista degli itinerari di tipo 'capuaniano'."""
    itinerari = Itinerario.objects.filter(is_active=True, tipo="capuaniano").order_by(
        "ordine", "translations__titolo"
    )

    # Prepara i dati per il template con serializzazione corretta
    itinerari_data = []
    for itinerario in itinerari:
        coordinate_tappe = (
            itinerario.coordinate_tappe if itinerario.coordinate_tappe else []
        )
        # Serializza l'intero oggetto itinerario per evitare problemi di escaping
        itinerario_json = json.dumps(
            {
                "slug": itinerario.slug,
                "titolo": itinerario.titolo,
                "descrizione_breve": (
                    " ".join(itinerario.descrizione.split()[:15]) + "..."
                    if itinerario.descrizione
                    else ""
                ),
                "colore": itinerario.colore_percorso or "#BF9B30",
                "icona": itinerario.icona_percorso or "📚",
                "durata": itinerario.durata_stimata or "",
                "difficolta": (
                    itinerario.get_difficolta_display() if itinerario.difficolta else ""
                ),
                "coordinate_tappe": coordinate_tappe,
            },
            ensure_ascii=False,
        )
        itinerari_data.append({"obj": itinerario, "itinerario_json": itinerario_json})

    context = {"itinerari": itinerari, "itinerari_data": itinerari_data}
    return render(request, "parco_verismo/itinerari_capuaniani.html", context)


def itinerari_tematici_view(request):
    """Lista degli itinerari di tipo 'tematico'."""
    itinerari = Itinerario.objects.filter(is_active=True, tipo="tematico").order_by(
        "ordine", "translations__titolo"
    )
    context = {"itinerari": itinerari}
    return render(request, "parco_verismo/itinerari_verghiani.html", context)


def itinerario_detail_view(request, slug):
    """Pagina di dettaglio di un singolo itinerario."""
    itinerario = get_object_or_404(Itinerario, slug=slug, is_active=True)
    context = {"itinerario": itinerario}
    return render(request, "parco_verismo/itinerario_detail.html", context)
