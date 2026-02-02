"""
Views per Itinerari Letterari - Sistema Rinnovato
"""

# Standard library imports
import json

# Django imports
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse

# Local imports
from ..models import Itinerario


def itinerari_verghiani_view(request):
    """
    View per gli itinerari verghiani con mappa interattiva e sidebar.
    """
    itinerari = Itinerario.objects.filter(
        is_active=True, 
        tipo="verghiano"
    ).prefetch_related('galleria').order_by("ordine")

    # Prepara i dati JSON per la mappa interattiva
    itinerari_data = []
    for itinerario in itinerari:
        itinerario_json = json.dumps({
            "id": itinerario.id,
            "slug": itinerario.slug,
            "titolo": itinerario.titolo,
            "descrizione": itinerario.descrizione,
            "descrizione_breve": (
                " ".join(itinerario.descrizione.split()[:20]) + "..."
                if itinerario.descrizione and len(itinerario.descrizione.split()) > 20
                else itinerario.descrizione or ""
            ),
            "colore_percorso": itinerario.colore_percorso,
            "durata_stimata": itinerario.durata_stimata or "Non specificata",
            "difficolta": itinerario.get_difficolta_display(),
            "coordinate_tappe": itinerario.coordinate_tappe or [],
            "percorsi_calcolati": itinerario.percorsi_calcolati or {},
            "centro_mappa": itinerario.get_centro_mappa(),
            "numero_tappe": itinerario.get_numero_tappe(),
            "url_detail": itinerario.get_absolute_url(),
            "link_maps": itinerario.link_maps,
            "url_immagine": itinerario.immagine.url if itinerario.immagine else None,
            "galleria_immagini": [img.immagine.url for img in itinerario.galleria.all()],
        }, ensure_ascii=False)
        
        itinerari_data.append({
            "obj": itinerario,
            "itinerario_json": itinerario_json
        })

    context = {
        "itinerari": itinerari,
        "itinerari_data": itinerari_data,
        "tipo_itinerario": "verghiano"
    }
    
    return render(request, "parco_verismo/itinerari_verghiani.html", context)


def itinerari_capuaniani_view(request):
    """
    View per gli itinerari capuaniani con mappa interattiva e sidebar.
    """
    itinerari = Itinerario.objects.filter(
        is_active=True, 
        tipo="capuaniano"
    ).prefetch_related('galleria').order_by("ordine")

    # Prepara i dati JSON per la mappa interattiva
    itinerari_data = []
    for itinerario in itinerari:
        itinerario_json = json.dumps({
            "id": itinerario.id,
            "slug": itinerario.slug,
            "titolo": itinerario.titolo,
            "descrizione": itinerario.descrizione,
            "descrizione_breve": (
                " ".join(itinerario.descrizione.split()[:20]) + "..."
                if itinerario.descrizione and len(itinerario.descrizione.split()) > 20
                else itinerario.descrizione or ""
            ),
            "colore_percorso": itinerario.colore_percorso,
            "durata_stimata": itinerario.durata_stimata or "Non specificata",
            "difficolta": itinerario.get_difficolta_display(),
            "coordinate_tappe": itinerario.coordinate_tappe or [],
            "percorsi_calcolati": itinerario.percorsi_calcolati or {},
            "centro_mappa": itinerario.get_centro_mappa(),
            "numero_tappe": itinerario.get_numero_tappe(),
            "url_detail": itinerario.get_absolute_url(),
            "link_maps": itinerario.link_maps,
            "url_immagine": itinerario.immagine.url if itinerario.immagine else None,
            "galleria_immagini": [img.immagine.url for img in itinerario.galleria.all()],
        }, ensure_ascii=False)
        
        itinerari_data.append({
            "obj": itinerario,
            "itinerario_json": itinerario_json
        })

    context = {
        "itinerari": itinerari,
        "itinerari_data": itinerari_data,
        "tipo_itinerario": "capuaniano"
    }
    
    return render(request, "parco_verismo/itinerari_capuaniani.html", context)


def itinerari_tematici_view(request):
    """
    View per gli itinerari tematici con mappa interattiva e sidebar.
    """
    itinerari = Itinerario.objects.filter(
        is_active=True, 
        tipo="tematico"
    ).prefetch_related('galleria').order_by("ordine")

    # Prepara i dati JSON per la mappa interattiva
    itinerari_data = []
    for itinerario in itinerari:
        itinerario_json = json.dumps({
            "id": itinerario.id,
            "slug": itinerario.slug,
            "titolo": itinerario.titolo,
            "descrizione": itinerario.descrizione,
            "descrizione_breve": (
                " ".join(itinerario.descrizione.split()[:20]) + "..."
                if itinerario.descrizione and len(itinerario.descrizione.split()) > 20
                else itinerario.descrizione or ""
            ),
            "colore_percorso": itinerario.colore_percorso,
            "durata_stimata": itinerario.durata_stimata or "Non specificata",
            "difficolta": itinerario.get_difficolta_display(),
            "coordinate_tappe": itinerario.coordinate_tappe or [],
            "percorsi_calcolati": itinerario.percorsi_calcolati or {},
            "centro_mappa": itinerario.get_centro_mappa(),
            "numero_tappe": itinerario.get_numero_tappe(),
            "url_detail": itinerario.get_absolute_url(),
            "link_maps": itinerario.link_maps,
            "url_immagine": itinerario.immagine.url if itinerario.immagine else None,
            "galleria_immagini": [img.immagine.url for img in itinerario.galleria.all()],
        }, ensure_ascii=False)
        
        itinerari_data.append({
            "obj": itinerario,
            "itinerario_json": itinerario_json
        })

    context = {
        "itinerari": itinerari,
        "itinerari_data": itinerari_data,
        "tipo_itinerario": "tematico"
    }
    
    return render(request, "parco_verismo/cammino_del_verismo.html", context)


def itinerario_detail_view(request, slug):
    """
    View per il dettaglio di un singolo itinerario con mappa delle tappe.
    """
    itinerario = get_object_or_404(Itinerario, slug=slug, is_active=True)
    
    # Prepara i dati per la mappa
    coordinate_json = json.dumps({
        "tappe": itinerario.get_tappe_ordinate(),
        "centro": itinerario.get_centro_mappa(),
        "colore": itinerario.colore_percorso,
    }, ensure_ascii=False)
    
    context = {
        "itinerario": itinerario,
        "tappe": itinerario.get_tappe_ordinate(),
        "numero_tappe": itinerario.get_numero_tappe(),
        "centro_mappa": itinerario.get_centro_mappa(),
        "coordinate_json": coordinate_json
    }
    
    return render(request, "parco_verismo/itinerario_detail.html", context)
