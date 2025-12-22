"""
Views per Documenti e Archivio Fotografico.
"""
# Django imports
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Local imports
from ..models import Documento, FotoArchivio


def documenti_view(request):
    """Mostra tutti i documenti e studi attivi con filtri per tipo e ricerca."""
    documenti = Documento.objects.filter(is_active=True).order_by('-data_pubblicazione')
    
    # Filtro per tipo
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter:
        documenti = documenti.filter(tipo=tipo_filter)
    
    # Ricerca
    query = request.GET.get('q', '')
    if query:
        documenti = documenti.filter(
            Q(translations__titolo__icontains=query) |
            Q(translations__descrizione__icontains=query) |
            Q(autori__icontains=query) |
            Q(translations__parole_chiave__icontains=query)
        ).distinct()
    
    context = {
        'documenti': documenti,
        'query': query,
        'tipo_filter': tipo_filter,
    }
    return render(request, 'parco_verismo/documenti.html', context)


def documento_detail_view(request, slug):
    """Pagina di dettaglio di un singolo documento/studio."""
    documento = get_object_or_404(Documento, slug=slug, is_active=True)
    context = {
        'documento': documento,
    }
    return render(request, 'parco_verismo/documento_detail.html', context)


def verga_capuana_fotografi_view(request):
    """Pagina dell'archivio fotografico con carosello e categorie."""
    foto_verga = FotoArchivio.objects.filter(is_active=True, autore='VERGA').order_by('ordine', '-data_aggiunta')
    foto_capuana = FotoArchivio.objects.filter(is_active=True, autore='CAPUANA').order_by('ordine', '-data_aggiunta')
    foto_altro = FotoArchivio.objects.filter(is_active=True).exclude(autore__in=['VERGA', 'CAPUANA']).order_by('ordine', '-data_aggiunta')
    
    # Raggruppa per categoria se necessario (opzionale, per ora lasciamo semplice)
    
    context = {
        'foto_verga': foto_verga,
        'foto_capuana': foto_capuana,
        'foto_altro': foto_altro,
    }
    return render(request, 'parco_verismo/verga_capuana_fotografi.html', context)
