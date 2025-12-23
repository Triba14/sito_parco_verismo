"""
Servizi business logic del Parco Letterario Giovanni Verga e Luigi Capuana.
"""

from .email_service import (
    invia_email_richiesta_confermata,
    invia_notifica_admin_nuova_richiesta,
)
from .search_service import (
    ricerca_opere,
    ricerca_documenti,
    get_eventi_futuri,
    get_notizie_recenti,
)
from .stats_service import (
    get_stats_richieste,
    get_stats_contenuti,
)

__all__ = [
    # Email
    "invia_email_richiesta_confermata",
    "invia_notifica_admin_nuova_richiesta",
    # Ricerca
    "ricerca_opere",
    "ricerca_documenti",
    "get_eventi_futuri",
    "get_notizie_recenti",
    # Statistiche
    "get_stats_richieste",
    "get_stats_contenuti",
]
