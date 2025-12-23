"""
Admin del Parco Letterario Giovanni Verga e Luigi Capuana.
Importa e registra tutti gli admin organizzati.
"""

# Importa tutti gli admin per registrarli automaticamente
from .biblioteca import AutoreAdmin, OperaAdmin
from .eventi import EventoAdmin, NotiziaAdmin
from .documenti import DocumentoAdmin, FotoArchivioAdmin
from .itinerari import ItinerarioAdmin, TappaItinerarioAdmin
from .richieste import RichiestaAdmin

# Gli admin sono già registrati con @admin.register nei rispettivi file
# Questo file serve solo per importarli tutti insieme

__all__ = [
    "AutoreAdmin",
    "OperaAdmin",
    "EventoAdmin",
    "NotiziaAdmin",
    "DocumentoAdmin",
    "FotoArchivioAdmin",
    "ItinerarioAdmin",
    "TappaItinerarioAdmin",
    "RichiestaAdmin",
]
