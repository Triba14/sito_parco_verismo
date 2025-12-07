#!/usr/bin/env python3
"""
Script unificato per popolare il database del Parco Letterario del Verismo.
Comprende: Autori, Opere (con copertine da Wikimedia), Eventi, Notizie, 
Archivio Fotografico, Itinerari con coordinate GPS.

Esegui con: python populate_database.py
"""
import os
import sys
import django
import json
import shutil
import urllib.request
import urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from parco_verismo.models import Autore, Opera, Evento, Notizia, FotoArchivio, Itinerario


# =============================================================================
# UTILITÀ
# =============================================================================

def copy_static_to_media(source_path, destination_relative):
    """Copia un file da static/assets/img a media/"""
    static_source = Path(settings.BASE_DIR) / 'parco_verismo' / 'static' / 'assets' / 'img' / source_path
    media_dest = Path(settings.MEDIA_ROOT) / destination_relative
    
    media_dest.parent.mkdir(parents=True, exist_ok=True)
    
    if static_source.exists():
        shutil.copy2(static_source, media_dest)
        return destination_relative
    return None


def download_wikimedia_image(url, save_path):
    """
    Scarica un'immagine da Wikimedia Commons (dominio pubblico/libero).
    Restituisce True se il download ha successo.
    """
    try:
        headers = {'User-Agent': 'ParcoVerismoBot/1.0 (educational project)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"  ⚠ Download fallito: {e}")
        return False


def print_section(title):
    print(f"\n{'='*70}")
    print(title)
    print('='*70)


# =============================================================================
# DATI: AUTORI
# =============================================================================

AUTORI = [
    {'nome': 'Giovanni Verga', 'slug': 'giovanni-verga'},
    {'nome': 'Luigi Capuana', 'slug': 'luigi-capuana'},
]


# =============================================================================
# DATI: OPERE (con URL copertine Wikimedia Commons - pubblico dominio)
# =============================================================================

OPERE_VERGA = [
    {
        'titolo': 'I Malavoglia',
        'slug': 'i-malavoglia',
        'anno': 1881,
        'trama': 'Romanzo corale che narra le vicende della famiglia Toscano, pescatori di Aci Trezza. Padron \'Ntoni cerca di mantenere unita la famiglia e ripagare un debito per l\'acquisto di lupini. Il naufragio della "Provvidenza" segna l\'inizio delle disgrazie familiari.',
        'analisi': 'Capolavoro del Verismo italiano. Verga usa il discorso indiretto libero e una lingua che riflette il parlato siciliano. Tema centrale: contrasto tra tradizione e modernità.',
        'link_wikisource': 'https://it.wikisource.org/wiki/I_Malavoglia',
        'copertina_url': None
    },
    {
        'titolo': 'Mastro-don Gesualdo',
        'slug': 'mastro-don-gesualdo',
        'anno': 1889,
        'trama': 'Storia di Gesualdo Motta, muratore arricchito che sposa una nobildonna decaduta. Non viene mai accettato dalla nobiltà, vivendo nella solitudine fino alla morte.',
        'analisi': 'Secondo romanzo del ciclo dei "Vinti". Analizza l\'impossibilità di superare le barriere di classe nella Sicilia dell\'Ottocento.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Mastro-don_Gesualdo',
        'copertina_url': None
    },
    {
        'titolo': 'Vita dei campi',
        'slug': 'vita-dei-campi',
        'anno': 1880,
        'trama': 'Raccolta di novelle sulla vita contadina siciliana: "Rosso Malpelo", "La Lupa", "Cavalleria rusticana" e altre storie di personaggi umili.',
        'analisi': 'Segna l\'inizio del verismo di Verga. Stile essenziale, visione pessimistica della lotta per la sopravvivenza.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1880)',
        'copertina_url': None
    },
    {
        'titolo': 'Novelle rusticane',
        'slug': 'novelle-rusticane',
        'anno': 1883,
        'trama': 'Include "La roba" (ossessione di Mazzarò per la ricchezza), "Libertà" (rivolta di Bronte), "Pane nero" e altre novelle.',
        'analisi': 'Approfondisce gli aspetti economici della vita rurale. Stile ancora più asciutto e impersonale.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_rusticane',
        'copertina_url': None
    },
    {
        'titolo': 'Storia di una capinera',
        'slug': 'storia-di-una-capinera',
        'anno': 1871,
        'trama': 'Romanzo epistolare sulla triste storia di Maria, costretta a prendere i voti. Lettere che rivelano sofferenze e un amore impossibile.',
        'analisi': 'Primo successo di Verga, ancora nel periodo romantico. Tono sentimentale e melodrammatico.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Storia_di_una_capinera',
        'copertina_url': None
    },
    {
        'titolo': 'Eva',
        'slug': 'eva-verga',
        'anno': 1873,
        'trama': 'Storia d\'amore tra Enrico Lanti ed Eva, una ballerina. Amore destinato a fallire per differenze sociali.',
        'analisi': 'Periodo romantico di Verga, con elementi che prefigurano il verismo.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Eva_(Verga)',
        'copertina_url': None
    },
    {
        'titolo': 'Tigre reale',
        'slug': 'tigre-reale',
        'anno': 1875,
        'trama': 'Storia d\'amore tra Giorgio La Ferlita e la contessa russa Natalia, detta "Tigre reale". Passione, tradimento e morte.',
        'analisi': 'Periodo romantico con spunti che anticipano il verismo nella caratterizzazione psicologica.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Tigre_reale',
        'copertina_url': None
    },
    {
        'titolo': 'Per le vie',
        'slug': 'per-le-vie',
        'anno': 1883,
        'trama': 'Novelle ambientate a Milano, personaggi umili travolti dai cambiamenti sociali ed economici.',
        'analisi': 'Verismo applicato al contesto urbano e industriale.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Per_le_vie',
        'copertina_url': None
    },
    {
        'titolo': 'Vagabondaggio',
        'slug': 'vagabondaggio',
        'anno': 1887,
        'trama': 'Novelle su emarginati e vagabondi ai margini della società.',
        'analisi': 'La modernità porta alienazione e solitudine, non progresso.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Vagabondaggio',
        'copertina_url': None
    },
    {
        'titolo': 'Don Candeloro e C.i',
        'slug': 'don-candeloro-e-ci',
        'anno': 1894,
        'trama': 'Novelle più leggere e umoristiche su una compagnia teatrale itinerante.',
        'analisi': 'Verga disteso e ironico, mostra versatilità stilistica.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Don_Candeloro_e_C.i',
        'copertina_url': None
    },
]

OPERE_CAPUANA = [
    {
        'titolo': 'Il marchese di Roccaverdina',
        'slug': 'il-marchese-di-roccaverdina',
        'anno': 1901,
        'trama': 'Il marchese uccide il marito della sua amante per gelosia. Il senso di colpa lo porta alla follia e alla confessione.',
        'analisi': 'Capolavoro di Capuana. Evoluzione del verismo verso l\'analisi psicologica, anticipa il decadentismo.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Il_marchese_di_Roccaverdina',
        'copertina_url': None
    },
    {
        'titolo': 'Giacinta',
        'slug': 'giacinta',
        'anno': 1879,
        'trama': 'Giovane donna traumatizzata da violenza infantile, cerca amore e accettazione. Matrimonio tormentato.',
        'analisi': 'Primo romanzo verista a trattare trauma e psicologia. Scandaloso per l\'epoca.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Giacinta',
        'copertina_url': None
    },
    {
        'titolo': 'Profili di donne',
        'slug': 'profili-di-donne',
        'anno': 1877,
        'trama': 'Ritratti femminili che esplorano caratteri, passioni e conflitti interiori.',
        'analisi': 'Interesse per la psicologia femminile e approccio analitico.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Profili_di_donne',
        'copertina_url': None
    },
    {
        'titolo': 'Scurpiddu',
        'slug': 'scurpiddu',
        'anno': 1898,
        'trama': 'Storia di un giovane siciliano e delle sue disavventure. Tono leggero e umoristico.',
        'analisi': 'Versatilità di Capuana, stile più personale.',
        'link_wikisource': 'https://it.wikisource.org/wiki/Scurpiddu',
        'copertina_url': None
    },
    {
        'titolo': 'C\'era una volta',
        'slug': 'cera-una-volta',
        'anno': 1882,
        'trama': 'Raccolta di fiabe siciliane tradizionali rielaborate da Capuana per i bambini.',
        'analisi': 'Opera importante nella letteratura per l\'infanzia italiana.',
        'link_wikisource': 'https://it.wikisource.org/wiki/C%27era_una_volta...',
        'copertina_url': None
    },
]


# =============================================================================
# DATI: ITINERARI CON COORDINATE GPS
# =============================================================================

ITINERARI = [
    {
        'titolo': 'Sulle tracce de I Malavoglia',
        'slug': 'itinerario-malavoglia',
        'descrizione': 'Percorso ad Aci Trezza: Casa del Nespolo, Faraglioni dei Ciclopi, le vie del borgo marinaro teatro delle vicende della famiglia Toscano.',
        'tipo': 'verghiano',
        'ordine': 1,
        'immagine_static': 'vizzini/centrostorico.jpg',
        'colore_percorso': '#1976D2',
        'icona_percorso': '🌊',
        'durata_stimata': '2 ore',
        'difficolta': 'facile',
        'coordinate_tappe': [
            {'nome': 'Casa del Nespolo', 'coords': [37.5614, 15.1595], 'descrizione': 'La casa della famiglia Malavoglia', 'order': 1},
            {'nome': 'Faraglioni dei Ciclopi', 'coords': [37.5589, 15.1642], 'descrizione': 'Iconici scogli di basalto', 'order': 2},
            {'nome': 'Chiesa S. Giovanni', 'coords': [37.5625, 15.1580], 'descrizione': 'Chiesa del paese', 'order': 3},
            {'nome': 'Porto di Aci Trezza', 'coords': [37.5605, 15.1620], 'descrizione': 'Il porto dei pescatori', 'order': 4},
        ]
    },
    {
        'titolo': 'Il mondo di Mastro-don Gesualdo',
        'slug': 'itinerario-mastro-don-gesualdo',
        'descrizione': 'Vizzini: palazzo nobiliare, centro storico, chiese barocche. Scenario del romanzo sulla stratificazione sociale siciliana.',
        'tipo': 'verghiano',
        'ordine': 2,
        'immagine_static': 'vizzini/borgo.jpg',
        'colore_percorso': '#8B4513',
        'icona_percorso': '🏛️',
        'durata_stimata': '3 ore',
        'difficolta': 'facile',
        'coordinate_tappe': [
            {'nome': 'Piazza Umberto I', 'coords': [37.1584, 14.7443], 'descrizione': 'Cuore del paese', 'order': 1},
            {'nome': 'Palazzo Verga', 'coords': [37.1578, 14.7438], 'descrizione': 'Dimora storica', 'order': 2},
            {'nome': 'Chiesa Madre', 'coords': [37.1590, 14.7450], 'descrizione': 'Chiesa barocca', 'order': 3},
            {'nome': 'Scalinata Santa Maria', 'coords': [37.1575, 14.7460], 'descrizione': 'Scenografia di Cavalleria Rusticana', 'order': 4},
        ]
    },
    {
        'titolo': 'I luoghi di Vita dei campi',
        'slug': 'itinerario-vita-dei-campi',
        'descrizione': 'Campagne siciliane: masserie, paesaggi rurali immutati, la Sicilia contadina dell\'Ottocento.',
        'tipo': 'verghiano',
        'ordine': 3,
        'immagine_static': 'vizzini/bosco.jpeg',
        'colore_percorso': '#388E3C',
        'icona_percorso': '🌾',
        'durata_stimata': '4 ore',
        'difficolta': 'media',
        'coordinate_tappe': [
            {'nome': 'Campagne di Vizzini', 'coords': [37.1700, 14.7500], 'descrizione': 'Paesaggi rurali', 'order': 1},
            {'nome': 'Antica Masseria', 'coords': [37.1650, 14.7600], 'descrizione': 'Architettura rurale', 'order': 2},
            {'nome': 'Bosco di Santo Pietro', 'coords': [37.1550, 14.7700], 'descrizione': 'Area boschiva', 'order': 3},
        ]
    },
    {
        'titolo': 'Da Vizzini ad Aci Trezza',
        'slug': 'itinerario-vizzini-aci-trezza',
        'descrizione': 'Percorso completo dalle colline dell\'entroterra al mare. Borghi, campagne e coste ioniche.',
        'tipo': 'verghiano',
        'ordine': 4,
        'immagine_static': 'vizzini/casaVerga.jpg',
        'colore_percorso': '#E65100',
        'icona_percorso': '🚗',
        'durata_stimata': '1 giorno',
        'difficolta': 'facile',
        'coordinate_tappe': [
            {'nome': 'Vizzini Centro', 'coords': [37.1584, 14.7443], 'descrizione': 'Partenza', 'order': 1},
            {'nome': 'Licodia Eubea', 'coords': [37.1543, 14.7016], 'descrizione': 'Borgo storico', 'order': 2},
            {'nome': 'Mineo', 'coords': [37.2650, 14.6900], 'descrizione': 'Patria di Capuana', 'order': 3},
            {'nome': 'Aci Trezza', 'coords': [37.5614, 15.1595], 'descrizione': 'Arrivo al mare', 'order': 4},
        ]
    },
    {
        'titolo': 'La Cunziria e il centro storico',
        'slug': 'itinerario-cunziria',
        'descrizione': 'Itinerario urbano: l\'antica conceria, Palazzo Verga, Duomo e le vie di Vizzini.',
        'tipo': 'verghiano',
        'ordine': 5,
        'immagine_static': 'vizzini/cunziria.jpg',
        'colore_percorso': '#C62828',
        'icona_percorso': '📖',
        'durata_stimata': '2 ore',
        'difficolta': 'facile',
        'coordinate_tappe': [
            {'nome': 'La Cunziria', 'coords': [37.1560, 14.7420], 'descrizione': 'Antica conceria', 'order': 1},
            {'nome': 'Palazzo Verga', 'coords': [37.1578, 14.7438], 'descrizione': 'Dimora della famiglia', 'order': 2},
            {'nome': 'Duomo di Vizzini', 'coords': [37.1590, 14.7455], 'descrizione': 'Chiesa principale', 'order': 3},
            {'nome': 'Piazza del Municipio', 'coords': [37.1582, 14.7448], 'descrizione': 'Centro del paese', 'order': 4},
        ]
    },
]


# =============================================================================
# DATI: EVENTI
# =============================================================================

EVENTI = [
    {
        'titolo': 'Festival del Verismo Siciliano',
        'slug': 'festival-verismo-2026',
        'descrizione': 'Evento annuale con spettacoli teatrali, conferenze, laboratori e degustazioni nei comuni del Parco.',
        'data_inizio': datetime(2026, 3, 15, 10, 0, tzinfo=ZoneInfo('Europe/Rome')),
        'data_fine': datetime(2026, 3, 17, 22, 0, tzinfo=ZoneInfo('Europe/Rome')),
        'luogo': 'Vizzini, Mineo, Licodia Eubea',
        'indirizzo': 'Comuni del Parco Letterario',
        'immagine_static': 'vizzini/festa.jpeg',
    },
    {
        'titolo': 'Lettura de I Malavoglia',
        'slug': 'lettura-malavoglia-2026',
        'descrizione': 'Serata speciale con lettura guidata e dibattito ad Aci Trezza.',
        'data_inizio': datetime(2026, 1, 20, 18, 30, tzinfo=ZoneInfo('Europe/Rome')),
        'data_fine': datetime(2026, 1, 20, 22, 0, tzinfo=ZoneInfo('Europe/Rome')),
        'luogo': 'Aci Trezza - Teatro Comunale',
        'indirizzo': 'Via Teatro, 1 - 95021 Aci Trezza (CT)',
        'immagine_static': 'vizzini/casaVerga.jpg',
    },
    {
        'titolo': 'Convegno: Il Verismo oggi',
        'slug': 'convegno-verismo-2026',
        'descrizione': 'Convegno internazionale sull\'attualità del verismo nella letteratura contemporanea.',
        'data_inizio': datetime(2026, 4, 25, 9, 30, tzinfo=ZoneInfo('Europe/Rome')),
        'data_fine': datetime(2026, 4, 25, 18, 0, tzinfo=ZoneInfo('Europe/Rome')),
        'luogo': 'Università di Catania',
        'indirizzo': 'Via Biblioteca, 4 - 95124 Catania',
        'immagine_static': 'vizzini/duomo.jpg',
    },
]


# =============================================================================
# DATI: NOTIZIE
# =============================================================================

NOTIZIE = [
    {
        'titolo': 'Inaugurazione mappa interattiva degli itinerari',
        'slug': 'mappa-interattiva-2025',
        'contenuto': 'È online la nuova mappa interattiva per esplorare gli itinerari verghiani con navigazione GPS.',
        'riassunto': 'Nuova mappa interattiva per esplorare gli itinerari letterari.',
        'immagine_static': 'vizzini/centrostorico.jpg',
    },
    {
        'titolo': 'Progetto educativo: Il verismo a scuola',
        'slug': 'verismo-scuola-2025',
        'contenuto': 'Visite guidate, laboratori e concorsi letterari per oltre 50 istituti scolastici siciliani.',
        'riassunto': 'Nuovo progetto educativo per portare il verismo nelle scuole.',
        'immagine_static': 'mineo/premio-luigi.jpg',
    },
    {
        'titolo': 'Restauro Casa Verga completato',
        'slug': 'restauro-casa-verga',
        'contenuto': 'Completato il restauro della casa natale di Verga a Vizzini, ora museo aperto al pubblico.',
        'riassunto': 'La casa natale di Verga diventa museo.',
        'immagine_static': 'vizzini/casaVerga.jpg',
    },
]


# =============================================================================
# FUNZIONI DI POPOLAMENTO
# =============================================================================

def populate_autori():
    print_section("AUTORI")
    for data in AUTORI:
        autore, created = Autore.objects.get_or_create(
            slug=data['slug'],
            defaults={'nome': data['nome']}
        )
        status = "✓ Creato" if created else "• Esistente"
        print(f"{status}: {autore.nome}")
    return {a['slug']: Autore.objects.get(slug=a['slug']) for a in AUTORI}


def populate_opere(autori):
    print_section("OPERE DI GIOVANNI VERGA")
    verga = autori['giovanni-verga']
    
    for data in OPERE_VERGA:
        opera, created = Opera.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'autore': verga,
                'anno_pubblicazione': data['anno'],
                'link_wikisource': data['link_wikisource']
            }
        )
        
        # Scarica copertina da Wikimedia se disponibile
        if data.get('copertina_url') and not opera.copertina:
            print(f"  ↓ Scarico copertina per {data['titolo']}...")
            temp_path = Path(settings.MEDIA_ROOT) / 'temp_cover.jpg'
            if download_wikimedia_image(data['copertina_url'], temp_path):
                with open(temp_path, 'rb') as f:
                    opera.copertina.save(f"{data['slug']}.jpg", File(f), save=False)
                temp_path.unlink(missing_ok=True)
        
        opera.set_current_language('it')
        opera.titolo = data['titolo']
        opera.trama = data['trama']
        opera.analisi = data['analisi']
        opera.save()
        
        status = "✓ Creata" if created else "• Aggiornata"
        print(f"{status}: {data['titolo']} ({data['anno']})")
    
    print_section("OPERE DI LUIGI CAPUANA")
    capuana = autori['luigi-capuana']
    
    for data in OPERE_CAPUANA:
        opera, created = Opera.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'autore': capuana,
                'anno_pubblicazione': data['anno'],
                'link_wikisource': data['link_wikisource']
            }
        )
        
        if data.get('copertina_url') and not opera.copertina:
            print(f"  ↓ Scarico copertina per {data['titolo']}...")
            temp_path = Path(settings.MEDIA_ROOT) / 'temp_cover.jpg'
            if download_wikimedia_image(data['copertina_url'], temp_path):
                with open(temp_path, 'rb') as f:
                    opera.copertina.save(f"{data['slug']}.jpg", File(f), save=False)
                temp_path.unlink(missing_ok=True)
        
        opera.set_current_language('it')
        opera.titolo = data['titolo']
        opera.trama = data['trama']
        opera.analisi = data['analisi']
        opera.save()
        
        status = "✓ Creata" if created else "• Aggiornata"
        print(f"{status}: {data['titolo']} ({data['anno']})")


def populate_itinerari():
    print_section("ITINERARI VERGHIANI")
    
    for data in ITINERARI:
        itinerario, created = Itinerario.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'tipo': data['tipo'],
                'ordine': data['ordine'],
                'colore_percorso': data['colore_percorso'],
                'icona_percorso': data['icona_percorso'],
                'durata_stimata': data['durata_stimata'],
                'difficolta': data['difficolta'],
                'coordinate_tappe': data['coordinate_tappe'],
                'is_active': True
            }
        )
        
        if not created:
            itinerario.colore_percorso = data['colore_percorso']
            itinerario.icona_percorso = data['icona_percorso']
            itinerario.durata_stimata = data['durata_stimata']
            itinerario.difficolta = data['difficolta']
            itinerario.coordinate_tappe = data['coordinate_tappe']
        
        # Copia immagine statica
        if data.get('immagine_static') and not itinerario.immagine:
            img_path = copy_static_to_media(data['immagine_static'], f"itinerari/{data['slug']}.jpg")
            if img_path:
                media_path = Path(settings.MEDIA_ROOT) / img_path
                with open(media_path, 'rb') as f:
                    itinerario.immagine.save(f"{data['slug']}.jpg", File(f), save=False)
        
        itinerario.set_current_language('it')
        itinerario.titolo = data['titolo']
        itinerario.descrizione = data['descrizione']
        itinerario.save()
        
        status = "✓ Creato" if created else "• Aggiornato"
        tappe = len(data['coordinate_tappe'])
        print(f"{status}: {data['titolo']} ({tappe} tappe)")


def populate_eventi():
    print_section("EVENTI")
    
    for data in EVENTI:
        evento, created = Evento.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'data_inizio': data['data_inizio'],
                'data_fine': data.get('data_fine'),
                'is_active': True
            }
        )
        
        if data.get('immagine_static') and not evento.immagine:
            img_path = copy_static_to_media(data['immagine_static'], f"eventi/{data['slug']}.jpg")
            if img_path:
                media_path = Path(settings.MEDIA_ROOT) / img_path
                with open(media_path, 'rb') as f:
                    evento.immagine.save(f"{data['slug']}.jpg", File(f), save=False)
        
        evento.set_current_language('it')
        evento.titolo = data['titolo']
        evento.descrizione = data['descrizione']
        evento.luogo = data['luogo']
        evento.indirizzo = data.get('indirizzo', '')
        evento.save()
        
        status = "✓ Creato" if created else "• Aggiornato"
        print(f"{status}: {data['titolo']} ({data['data_inizio'].date()})")


def populate_notizie():
    print_section("NOTIZIE")
    
    for data in NOTIZIE:
        notizia, created = Notizia.objects.get_or_create(
            slug=data['slug'],
            defaults={'is_active': True}
        )
        
        if data.get('immagine_static') and not notizia.immagine:
            img_path = copy_static_to_media(data['immagine_static'], f"notizie/{data['slug']}.jpg")
            if img_path:
                media_path = Path(settings.MEDIA_ROOT) / img_path
                with open(media_path, 'rb') as f:
                    notizia.immagine.save(f"{data['slug']}.jpg", File(f), save=False)
        
        notizia.set_current_language('it')
        notizia.titolo = data['titolo']
        notizia.contenuto = data['contenuto']
        notizia.riassunto = data['riassunto']
        notizia.save()
        
        status = "✓ Creata" if created else "• Aggiornata"
        print(f"{status}: {data['titolo']}")


def print_summary():
    print_section("RIEPILOGO")
    print(f"Autori:     {Autore.objects.count()}")
    print(f"Opere:      {Opera.objects.count()}")
    print(f"  - Verga:  {Opera.objects.filter(autore__slug='giovanni-verga').count()}")
    print(f"  - Capuana:{Opera.objects.filter(autore__slug='luigi-capuana').count()}")
    print(f"Itinerari:  {Itinerario.objects.count()}")
    print(f"Eventi:     {Evento.objects.count()}")
    print(f"Notizie:    {Notizia.objects.count()}")
    print(f"\n✅ Database popolato con successo!")
    print(f"\nAvvia il server: python manage.py runserver")
    print(f"Homepage: http://127.0.0.1:8000/")


def main():
    print("="*70)
    print("POPOLAMENTO DATABASE - PARCO LETTERARIO DEL VERISMO")
    print("="*70)
    
    # Crea directory media se non esiste
    Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
    
    autori = populate_autori()
    populate_opere(autori)
    populate_itinerari()
    populate_eventi()
    populate_notizie()
    print_summary()


if __name__ == '__main__':
    main()
