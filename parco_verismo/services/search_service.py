"""
Servizi per ricerche e filtri.
"""

from django.db.models import Q


def ricerca_opere(query, queryset=None):
    """
    Effettua una ricerca nelle opere per titolo o autore.

    Args:
        query: Stringa di ricerca
        queryset: QuerySet base (opzionale)

    Returns:
        QuerySet filtrato
    """
    from ..models import Opera

    if queryset is None:
        queryset = Opera.objects.all()

    if not query:
        return queryset

    return queryset.filter(
        Q(translations__titolo__icontains=query)
        | Q(autore__nome__icontains=query)
        | Q(translations__trama__icontains=query)
    ).distinct()


def ricerca_documenti(query, tipo=None, queryset=None):
    """
    Effettua una ricerca nei documenti.

    Args:
        query: Stringa di ricerca
        tipo: Tipo di documento (opzionale)
        queryset: QuerySet base (opzionale)

    Returns:
        QuerySet filtrato
    """
    from ..models import Documento

    if queryset is None:
        queryset = Documento.objects.filter(is_active=True)

    if tipo:
        queryset = queryset.filter(tipo=tipo)

    if query:
        queryset = queryset.filter(
            Q(translations__titolo__icontains=query)
            | Q(translations__descrizione__icontains=query)
            | Q(autori__icontains=query)
            | Q(translations__parole_chiave__icontains=query)
        ).distinct()

    return queryset


def get_eventi_futuri(limit=None):
    """
    Restituisce gli eventi futuri attivi.

    Args:
        limit: Numero massimo di eventi da restituire

    Returns:
        QuerySet di eventi
    """
    from django.utils import timezone
    from ..models import Evento

    eventi = Evento.objects.filter(
        is_active=True, data_inizio__gte=timezone.now()
    ).order_by("data_inizio")

    if limit:
        eventi = eventi[:limit]

    return eventi


def get_notizie_recenti(limit=None):
    """
    Restituisce le notizie più recenti.

    Args:
        limit: Numero massimo di notizie da restituire

    Returns:
        QuerySet di notizie
    """
    from ..models import Notizia

    notizie = Notizia.objects.filter(is_active=True).order_by("-data_pubblicazione")

    if limit:
        notizie = notizie[:limit]

    return notizie
