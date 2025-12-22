"""
Servizi per statistiche e report.
"""

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta


def get_stats_richieste():
    """
    Restituisce statistiche sulle richieste.

    Returns:
        Dict con le statistiche
    """
    from ..models import Richiesta

    oggi = timezone.now().date()
    settimana_fa = oggi - timedelta(days=7)
    mese_fa = oggi - timedelta(days=30)

    stats = {
        "totali": Richiesta.objects.count(),
        "nuove": Richiesta.objects.filter(stato="nuova").count(),
        "in_lavorazione": Richiesta.objects.filter(stato="in_lavorazione").count(),
        "confermate": Richiesta.objects.filter(stato="confermata").count(),
        "completate": Richiesta.objects.filter(stato="completata").count(),
        "questa_settimana": Richiesta.objects.filter(
            data_richiesta__gte=settimana_fa
        ).count(),
        "questo_mese": Richiesta.objects.filter(data_richiesta__gte=mese_fa).count(),
        "per_priorita": Richiesta.objects.values("priorita").annotate(count=Count("id")).order_by("-count"),
    }

    return stats


def get_stats_contenuti():
    """
    Restituisce statistiche sui contenuti pubblicati.

    Returns:
        Dict con le statistiche
    """
    from ..models import Opera, Evento, Notizia, Documento, Itinerario

    stats = {
        "opere": Opera.objects.count(),
        "eventi": Evento.objects.filter(is_active=True).count(),
        "notizie": Notizia.objects.filter(is_active=True).count(),
        "documenti": Documento.objects.filter(is_active=True).count(),
        "itinerari": Itinerario.objects.filter(is_active=True).count(),
    }

    return stats
