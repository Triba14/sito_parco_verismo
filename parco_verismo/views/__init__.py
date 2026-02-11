"""
Views del Parco Letterario Giovanni Verga e Luigi Capuana.
Organizzate per funzionalità e dominio.
"""

# Homepage
from .home import home_view

# Biblioteca
from .biblioteca import (
    opere_per_autore_view,
    personaggi_lessico_view,
    luoghi_opere_view,
)

# Eventi e Notizie
from .eventi import (
    eventi_view,
    evento_detail_view,
    notizie_view,
    notizia_detail_view,
)

# Documenti e Archivio
from .documenti import (
    documenti_view,
    documento_detail_view,
    verga_capuana_fotografi_view,
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

# Error Handlers
from .errors import (
    custom_404,
    custom_500,
    custom_403,
    custom_400,
)

__all__ = [
    # Home
    'home_view',
    # Biblioteca
    'opere_per_autore_view',
    # Eventi e Notizie
    'eventi_view',
    'evento_detail_view',
    'notizie_view',
    'notizia_detail_view',
    # Documenti
    'documenti_view',
    'documento_detail_view',
    'verga_capuana_fotografi_view',
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
    # Error handlers
    'custom_404',
    'custom_500',
    'custom_403',
    'custom_400',
]
