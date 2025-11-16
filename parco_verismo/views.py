from django.shortcuts import render, get_object_or_404
from .models import Opera, Autore, Evento, Notizia, Documento, FotoArchivio
from django.db.models import Q
from django.http import HttpResponse

def home_view(request):
    return render(request, 'parco_verismo/index.html')

def biblioteca_view(request):
    """
    Mostra tutte le opere e gestisce la ricerca.
    """
    query = request.GET.get('q', '')
    opere_list = Opera.objects.all()

    if query:
        # Cerca nel titolo dell'opera O nel nome dell'autore
        opere_list = opere_list.filter(
            Q(translations__titolo__icontains=query) | Q(autore__nome__icontains=query)
        ).distinct()

    context = {
        'opere': opere_list,
        'query': query,
    }
    return render(request, 'parco_verismo/biblioteca.html', context)

def opere_per_autore_view(request, autore_slug):
    """
    Pagina di presentazione per le opere di un singolo autore (es. Opere di Verga).
    """
    autore = get_object_or_404(Autore, slug=autore_slug)
    opere_autore = Opera.objects.filter(autore=autore)
    context = {
        'autore': autore,
        'opere': opere_autore,
    }
    return render(request, 'parco_verismo/opere_per_autore.html', context)

def opera_detail_view(request, slug):
    """
    Pagina di presentazione della singola opera con trama, analisi e link finale.
    """
    opera = get_object_or_404(Opera, slug=slug)
    context = {
        'opera': opera,
    }
    return render(request, 'parco_verismo/opera_detail.html', context)


def eventi_view(request):
    """
    Mostra tutti gli eventi attivi ordinati per data.
    """
    from django.utils import timezone
    eventi = Evento.objects.filter(is_active=True, data_inizio__gte=timezone.now()).order_by('data_inizio')
    context = {
        'eventi': eventi,
    }
    return render(request, 'parco_verismo/eventi.html', context)


def calendario_view(request):
    """
    Mostra il calendario degli eventi.
    """
    from django.utils import timezone
    eventi = Evento.objects.filter(is_active=True).order_by('data_inizio')
    context = {
        'eventi': eventi,
    }
    return render(request, 'parco_verismo/calendario.html', context)


def evento_detail_view(request, slug):
    """
    Pagina di dettaglio di un singolo evento.
    """
    evento = get_object_or_404(Evento, slug=slug, is_active=True)
    context = {
        'evento': evento,
    }
    return render(request, 'parco_verismo/evento_detail.html', context)


def notizie_view(request):
    """
    Mostra tutte le notizie attive ordinate per data di pubblicazione.
    """
    notizie = Notizia.objects.filter(is_active=True).order_by('-data_pubblicazione')
    context = {
        'notizie': notizie,
    }
    return render(request, 'parco_verismo/notizie.html', context)


def notizia_detail_view(request, slug):
    """
    Pagina di dettaglio di una singola notizia.
    """
    notizia = get_object_or_404(Notizia, slug=slug, is_active=True)
    context = {
        'notizia': notizia,
    }
    return render(request, 'parco_verismo/notizia_detail.html', context)


def documenti_view(request):
    """
    Mostra tutti i documenti e studi attivi ordinati per data di pubblicazione.
    Supporta anche la ricerca per titolo, descrizione e autori.
    """
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
    """
    Pagina di dettaglio di un singolo documento/studio.
    """
    documento = get_object_or_404(Documento, slug=slug, is_active=True)
    context = {
        'documento': documento,
    }
    return render(request, 'parco_verismo/documento_detail.html', context)


def archivio_fotografico_view(request):
    """
    Pagina dell'archivio fotografico con carosello.
    """
    foto = FotoArchivio.objects.filter(is_active=True).order_by('ordine', '-data_aggiunta')
    
    # Raggruppa per categoria se necessario
    categorie = foto.values_list('categoria', flat=True).distinct().exclude(categoria__isnull=True).exclude(categoria='')
    
    context = {
        'foto': foto,
        'categorie': categorie,
    }
    return render(request, 'parco_verismo/archivio_fotografico.html', context)
