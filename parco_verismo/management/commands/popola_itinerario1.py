"""
Management command per popolare il database con un itinerario di esempio.
Uso: python manage.py popola_itinerario1
"""

from django.core.management.base import BaseCommand
from django.utils import translation
from parco_verismo.models.itinerari import Itinerario


class Command(BaseCommand):
    help = 'Popola il database con un itinerario verghiano di esempio (Catania Verghiana)'

    def handle(self, *args, **options):
        # Attiva la lingua italiana per le traduzioni
        translation.activate('it')
        
        self.stdout.write('Inizio popolamento itinerario...')
        
        # Dati dell'itinerario
        slug = 'catania-verghiana'
        
        # Controlla se esiste già
        if Itinerario.objects.filter(slug=slug).exists():
            self.stdout.write(
                self.style.WARNING(f'Itinerario "{slug}" già esistente. Elimino e ricreo...')
            )
            Itinerario.objects.filter(slug=slug).delete()
        
        # Coordinate delle tappe (Catania Verghiana)
        coordinate_tappe = [
            {
                "nome": "Casa del Nespolo",
                "coords": [37.5029, 15.0876],
                "descrizione_breve": "La casa di famiglia dei Malavoglia",
                "descrizione": "La celebre Casa del Nespolo, immortalata nel capolavoro verghiano 'I Malavoglia'. Qui viveva la famiglia di pescatori protagonista del romanzo, simbolo delle tradizioni e dei valori della Sicilia marinara dell'Ottocento.",
                "order": 1
            },
            {
                "nome": "Piazza San Francesco",
                "coords": [37.5025, 15.0872],
                "descrizione_breve": "La piazza del paese di Aci Trezza",
                "descrizione": "Il cuore pulsante di Aci Trezza, dove si svolgeva la vita quotidiana del paese. Qui i personaggi de 'I Malavoglia' si incontravano, discutevano e vivevano i loro drammi quotidiani. La piazza conserva ancora l'atmosfera dell'epoca verghiana.",
                "order": 2
            },
            {
                "nome": "Porto di Aci Trezza",
                "coords": [37.5018, 15.0894],
                "descrizione_breve": "Il porto dei pescatori",
                "descrizione": "Il porto da cui partivano le barche dei pescatori, tra cui la 'Provvidenza' dei Malavoglia. Luogo centrale nella narrazione verghiana, teatro di partenze, ritorni e tragedie del mare. Ancora oggi è possibile ammirare i Faraglioni dei Ciclopi che dominano il paesaggio marino.",
                "order": 3
            },
            {
                "nome": "Faraglioni dei Ciclopi",
                "coords": [37.5008, 15.0905],
                "descrizione_breve": "Gli scogli leggendari",
                "descrizione": "I mitici Faraglioni scagliati da Polifemo contro Ulisse secondo la leggenda omerica. Questi scogli maestosi rappresentano lo sfondo naturale immutabile delle vicende umane narrate da Verga, simbolo della potenza della natura di fronte alla fragilità dell'uomo.",
                "order": 4
            },
            {
                "nome": "Chiesa di San Giovanni Battista",
                "coords": [37.5034, 15.0868],
                "descrizione_breve": "La chiesa del paese",
                "descrizione": "La chiesa parrocchiale di Aci Trezza, luogo di ritrovo della comunità e scenario di momenti importanti della vita religiosa e sociale del paese. Nel romanzo verghiano, rappresenta il punto di riferimento spirituale e morale della comunità.",
                "order": 5
            },
            {
                "nome": "Casa Museo Giovanni Verga",
                "coords": [37.5065, 15.0877],
                "descrizione_breve": "La casa natale dello scrittore a Catania",
                "descrizione": "L'abitazione dove nacque Giovanni Verga nel 1840 a Catania, oggi museo dedicato alla vita e alle opere del grande scrittore. Il museo conserva arredi originali, manoscritti, fotografie e oggetti personali che testimoniano la vita di Verga e l'ambiente culturale della Sicilia ottocentesca.",
                "order": 6
            }
        ]
        
        # Percorsi calcolati tra le tappe (simulazione OSRM)
        percorsi_calcolati = {
            "0-1": {
                "coordinates": [
                    [15.0876, 37.5029],
                    [15.0874, 37.5027],
                    [15.0872, 37.5025]
                ],
                "distance": 450,
                "duration": 360
            },
            "1-2": {
                "coordinates": [
                    [15.0872, 37.5025],
                    [15.0880, 37.5022],
                    [15.0894, 37.5018]
                ],
                "distance": 320,
                "duration": 280
            },
            "2-3": {
                "coordinates": [
                    [15.0894, 37.5018],
                    [15.0900, 37.5012],
                    [15.0905, 37.5008]
                ],
                "distance": 280,
                "duration": 240
            },
            "3-4": {
                "coordinates": [
                    [15.0905, 37.5008],
                    [15.0890, 37.5020],
                    [15.0868, 37.5034]
                ],
                "distance": 520,
                "duration": 420
            },
            "4-5": {
                "coordinates": [
                    [15.0868, 37.5034],
                    [15.0870, 37.5045],
                    [15.0875, 37.5055],
                    [15.0877, 37.5065]
                ],
                "distance": 850,
                "duration": 660
            }
        }
        
        # Crea l'itinerario
        itinerario = Itinerario.objects.create(
            slug=slug,
            tipo='verghiano',
            ordine=1,
            durata_stimata='3-4 ore',
            difficolta='facile',
            coordinate_tappe=coordinate_tappe,
            percorsi_calcolati=percorsi_calcolati,
            colore_percorso='#4A6741',
            link_maps='https://goo.gl/maps/esempio',
            is_active=True
        )
        
        # Traduzioni italiane
        itinerario.translations.create(
            language_code='it',
            titolo='Catania Verghiana - Sulle tracce de I Malavoglia',
            descrizione=(
                'Un affascinante percorso letterario che ripercorre i luoghi immortalati '
                'da Giovanni Verga nel suo capolavoro "I Malavoglia". Da Aci Trezza, con la '
                'celebre Casa del Nespolo e i mitici Faraglioni dei Ciclopi, fino alla casa '
                'natale dello scrittore a Catania.\n\n'
                'Lungo questo itinerario potrete immergervi nell\'atmosfera dell\'Ottocento '
                'siciliano, scoprendo i luoghi che hanno ispirato il grande scrittore verista '
                'e che ancora oggi conservano intatto il loro fascino. Dalle strade del '
                'piccolo borgo marinaro di Aci Trezza, teatro delle vicende dei Malavoglia, '
                'ai vicoli di Catania dove nacque Verga, questo percorso è un viaggio nella '
                'Sicilia autentica e nelle radici del verismo letterario italiano.'
            ),
            note=(
                'INFORMAZIONI PRATICHE:\n\n'
                '• Il percorso si può effettuare a piedi o in auto\n'
                '• Durata consigliata: 3-4 ore (con visite ai musei)\n'
                '• Difficoltà: Facile, adatto a tutti\n'
                '• Periodo migliore: Primavera e autunno per il clima mite\n'
                '• Parcheggio: Disponibile ad Aci Trezza e a Catania\n\n'
                'PUNTI DI INTERESSE:\n'
                '• Casa del Nespolo: edificio storico, visibile esternamente\n'
                '• Museo Casa Verga: visita guidata consigliata (prenotazione consigliata)\n'
                '• Faraglioni dei Ciclopi: vista panoramica dal lungomare\n\n'
                'CONSIGLI:\n'
                '• Iniziare il percorso al mattino per godere della luce migliore\n'
                '• Portare con sé una copia de "I Malavoglia" per rileggere alcuni passi '
                'nei luoghi originali\n'
                '• Assaggiare le specialità locali nei ristorantini di Aci Trezza\n'
                '• Prenotare la visita al Museo Casa Verga con anticipo nei weekend'
            )
        )
        
        # Traduzioni inglesi
        itinerario.translations.create(
            language_code='en',
            titolo='Verga\'s Catania - Following the Malavoglia Trail',
            descrizione=(
                'A fascinating literary route that traces the places immortalized by '
                'Giovanni Verga in his masterpiece "I Malavoglia" (The House by the Medlar Tree). '
                'From Aci Trezza, with the famous House by the Medlar Tree and the mythical '
                'Cyclops Stacks, to the writer\'s birthplace in Catania.\n\n'
                'Along this itinerary you can immerse yourself in the atmosphere of '
                '19th-century Sicily, discovering the places that inspired the great verismo '
                'writer and which still retain their charm today. From the streets of the '
                'small fishing village of Aci Trezza, setting of the Malavoglia story, to '
                'the alleys of Catania where Verga was born, this route is a journey into '
                'authentic Sicily and the roots of Italian literary verismo.'
            ),
            note=(
                'PRACTICAL INFORMATION:\n\n'
                '• The route can be done on foot or by car\n'
                '• Recommended duration: 3-4 hours (including museum visits)\n'
                '• Difficulty: Easy, suitable for everyone\n'
                '• Best period: Spring and autumn for mild weather\n'
                '• Parking: Available in Aci Trezza and Catania\n\n'
                'POINTS OF INTEREST:\n'
                '• House by the Medlar Tree: historic building, visible from outside\n'
                '• Verga House Museum: guided tour recommended (booking advised)\n'
                '• Cyclops Stacks: panoramic view from the promenade\n\n'
                'TIPS:\n'
                '• Start the route in the morning for the best light\n'
                '• Bring a copy of "I Malavoglia" to reread some passages in the '
                'original locations\n'
                '• Taste local specialties in Aci Trezza\'s small restaurants\n'
                '• Book the visit to Verga House Museum in advance on weekends'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Itinerario "{itinerario}" creato con successo!\n'
                f'  - Tipo: {itinerario.tipo}\n'
                f'  - Tappe: {itinerario.get_numero_tappe()}\n'
                f'  - Durata: {itinerario.durata_stimata}\n'
                f'  - Difficoltà: {itinerario.difficolta}\n'
                f'  - Slug: {itinerario.slug}\n\n'
                f'NOTA: Le immagini del carosello vanno aggiunte manualmente tramite '
                f'l\'admin Django.\n'
                f'Per aggiungere immagini alla galleria:\n'
                f'  1. Accedi all\'admin: /admin/\n'
                f'  2. Vai su "Itinerari" > "{itinerario}"\n'
                f'  3. Scorri fino a "Immagini Galleria" e aggiungi le immagini\n'
            )
        )
        
        translation.deactivate()
