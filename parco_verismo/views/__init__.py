"""
Views del Parco Letterario del Verismo.
Organizzate per funzionalità e dominio.
"""

# Homepage
from .home import home_view

# Biblioteca
from .biblioteca import (
    biblioteca_view,
    opere_per_autore_view,
    opera_detail_view,
)

# Eventi e Notizie
from .eventi import (
    eventi_view,
    calendario_view,
    evento_detail_view,
    notizie_view,
    notizia_detail_view,
)

# Documenti e Archivio
from .documenti import (
    documenti_view,
    documento_detail_view,
    archivio_fotografico_view,
)

# Itinerari
from .itinerari import (
    itinerari_verghiani_view,
    itinerari_capuaniani_view,
    itinerari_tematici_view,
    itinerario_detail_view,
)

# Comuni
from .comuni import (
    licodia_view,
    mineo_view,
    vizzini_view,
)

# Pagine Istituzionali
from .istituzionale import (
    missione_visione_view,
    comitato_tecnico_scientifico_view,
    comitato_regolamento_view,
    regolamenti_documenti_view,
    partner_rete_territoriale_view,
    accrediti_finanziamenti_view,
    contatti_view,
    privacy_policy_view,
    note_legali_view,
    cookie_policy_view,
)

__all__ = [
    # Home
    'home_view',
    # Biblioteca
    'biblioteca_view',
    'opere_per_autore_view',
    'opera_detail_view',
    # Eventi e Notizie
    'eventi_view',
    'calendario_view',
    'evento_detail_view',
    'notizie_view',
    'notizia_detail_view',
    # Documenti
    'documenti_view',
    'documento_detail_view',
    'archivio_fotografico_view',
    # Itinerari
    'itinerari_verghiani_view',
    'itinerari_capuaniani_view',
    'itinerari_tematici_view',
    'itinerario_detail_view',
    # Comuni
    'licodia_view',
    'mineo_view',
    'vizzini_view',
    # Istituzionali
    'missione_visione_view',
    'comitato_tecnico_scientifico_view',
    'comitato_regolamento_view',
    'regolamenti_documenti_view',
    'partner_rete_territoriale_view',
    'accrediti_finanziamenti_view',
    'contatti_view',
    'privacy_policy_view',
    'note_legali_view',
    'cookie_policy_view',
]
