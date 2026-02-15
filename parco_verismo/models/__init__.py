"""
Modelli del Parco Letterario Giovanni Verga e Luigi Capuana.
Organizzati per funzionalità e dominio.
"""

# Import tutti i modelli per renderli disponibili
from .autori_opere import Autore, Opera, LuogoLetterario, OperaInLuogo
from .eventi import Evento, Notizia, EventoImage, NotiziaImage, EventoDocumento, NotiziaDocumento
from .documenti import Documento, FotoArchivio
from .itinerari import Itinerario, ItinerarioImmagine
from .richieste import Richiesta
from .ristoranti import Ristorante

# Esporta tutti i modelli
__all__ = [
    # Biblioteca
    "Autore",
    "Opera",
    "LuogoLetterario",
    "OperaInLuogo",
    # Eventi e Notizie
    "Evento",
    "EventoImage",
    "EventoDocumento",
    "Notizia",
    "NotiziaImage",
    "NotiziaDocumento",
    # Documenti e Archivio
    "Documento",
    "FotoArchivio",
    # Itinerari
    "Itinerario",
    "ItinerarioImmagine",
    # Richieste di contatto
    "Richiesta",
    # Ristoranti
    "Ristorante",
]
