"""
Modelli del Parco Letterario Giovanni Verga e Luigi Capuana.
Organizzati per funzionalità e dominio.
"""

# Import tutti i modelli per renderli disponibili
from .autori_opere import Autore, Opera
from .eventi import Evento, Notizia
from .documenti import Documento, FotoArchivio
from .itinerari import Itinerario, TappaItinerario
from .richieste import Richiesta

# Esporta tutti i modelli
__all__ = [
    # Biblioteca
    "Autore",
    "Opera",
    # Eventi e Notizie
    "Evento",
    "Notizia",
    # Documenti e Archivio
    "Documento",
    "FotoArchivio",
    # Itinerari
    "Itinerario",
    "TappaItinerario",
    # Richieste di contatto
    "Richiesta",
]
