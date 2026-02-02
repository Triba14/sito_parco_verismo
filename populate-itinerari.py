#!/usr/bin/env python3
"""
Script dedicato per popolare SOLO gli itinerari nel database del Parco Letterario.
Usa i dati esattamente come definiti in itinerari_data senza modificarli.

Esegui con: python populate-itinerari.py
"""
import os
import django
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Itinerario
from django.conf import settings
from django.core.files import File


def copy_static_to_media(source_path, destination_relative):
    """
    Copia un file da static/assets/img a media/ e restituisce il percorso del file copiato
    """
    if not source_path:
        return None
        
    static_source = os.path.join(settings.BASE_DIR, 'parco_verismo', 'static', 'assets', 'img', source_path)
    media_dest = os.path.join(settings.MEDIA_ROOT, destination_relative)
    
    # Crea la directory se non esiste
    os.makedirs(os.path.dirname(media_dest), exist_ok=True)
    
    if os.path.exists(static_source):
        try:
            shutil.copy2(static_source, media_dest)
            # Restituisce il percorso relativo per usarlo con Django File
            return destination_relative
        except Exception as e:
            print(f"  ⚠️  Errore copia immagine {source_path}: {e}")
            return None
    else:
        print(f"  ⚠️  Immagine non trovata: {source_path}")
    return None


def populate_itinerari():
    print("="*70)
    print("POPOLAMENTO ITINERARI")
    print("="*70)
    
    itinerari_data = [
        {
            'titolo': 'Vizzini – 1° Itinerario: Luoghi, paesaggi e memorie',
            'slug': 'itinerario-verghiano-vizzini-1',
            'descrizione': "Itinerario urbano che attraversa il centro storico di Vizzini, ricostruendo i luoghi reali, familiari e narrativi legati alla vita e alle opere di Giovanni Verga, con particolare riferimento alla produzione verista e alla documentazione fotografica realizzata dallo scrittore alla fine dell'Ottocento.",
            'tipo': 'verghiano',
            'ordine': 1,
            'durata_stimata': '2-3 ore',
            'difficolta': 'facile',
            'is_active': True,
            'link_maps': 'https://maps.app.goo.gl/T8Ef5Tzgv5yKsTHu6',
            'colore_percorso': '#B22222',
            'immagine_path': 'itinerari/vizzini-verga-1.jpg',
            'coordinate_tappe': [
                {
                    'nome': '1ª tappa - Piazza Umberto I',
                    'coords': [37.16144617637193, 14.748882339392699],
                    'descrizione_breve': 'La storica piazza centrale con i palazzi nobiliari.',
                    'descrizione': "È la storica piazza centrale della città, su cui si affaccia il Palazzo Municipale. Sullo stesso spazio prospettavano l'antico Collegio Gesuitico e la chiesa di Sant'Ippolito, demoliti agli inizi del Novecento per la costruzione delle scuole pubbliche. Comprende: Palazzo Verga-Catalano, dimora della famiglia dello scrittore riedificata a metà Ottocento dallo zio don Salvatore Verga Catalano in stile neoclassico; Palazzo Sganci (Palazzo La Rocca), dimora settecentesca dove Verga ambienta l'incontro tra Bianca Trao e Gesualdo Motta; Casa Senatoria, edificio tardo barocco completato nel 1800 su progetto dell'architetto Corrado Mazza di Noto. \r\n\r\n<b>Riferimenti letterari:</b> «La signora Sganci aveva la casa piena di gente... i cinque balconi che mandavano fuoco e fiamma sulla piazza nera di popolo» (Mastro-don Gesualdo).",
                    'order': 1,
                    'tratteggiato': False
                },
                {
                    'nome': '2ª tappa - Via Lombarda – Belvedere',
                    'coords': [37.16207068655397, 14.747091032580343],
                    'descrizione_breve': "Punto panoramico sulla Cunziria e i quartieri verghiani.",
                    'descrizione': "Punto panoramico strategico su: La Cunziria, borgo di archeologia industriale per la conciatura delle pelli con circa quaranta edifici e la chiesa di Sant'Eligio; la Strada Nazionale (SS124), percorsa da Jeli con la sua mandria; la Via della Masera, antica via verso Palermo percorsa dalla lettiga di Gesualdo; il quartiere Sant'Antonio, sede della casa di Mara. \r\n\r\n<b>Riferimenti letterari:</b> «Prima di giorno si prese il suo coltello a molla... e si mise in cammino pei fichidindia della Canziria» (Cavalleria Rusticana). «Dalla svolta dello stradone si cominciava a scorgere il paese...» (Jeli il pastore).",
                    'order': 2,
                    'tratteggiato': False
                },
                {
                    'nome': '3ª tappa - Largo Matrice',
                    'coords': [37.16097133953088, 14.744352384792107],
                    'descrizione_breve': 'Chiesa Madre, Basilica di San Vito e il Bastione.',
                    'descrizione': "Include la Chiesa Madre di San Gregorio Magno, con portale gotico-catalano e tele di Filippo Paladini, e la Basilica di San Vito, edificio tardo barocco con influssi manieristi che custodisce un Cristo ligneo seicentesco e un reliquiario del 1601. Comprende anche il Bastione di San Vito come punto panoramico sulla valle. \r\n\r\n<b>Riferimenti letterari:</b> «...il santo tornò in chiesa a corsa piuttosto che a passo di processione, e la festa finì come le commedie di Pulcinella» (Guerra di santi).",
                    'order': 3,
                    'tratteggiato': False
                },
                {
                    'nome': '4ª tappa - Via Etrusca – S. Maria dei Greci',
                    'coords': [37.16094010321448, 14.745547583869696],
                    'descrizione_breve': "Chiesa e monastero legati a Storia di una Capinera.",
                    'descrizione': "Una delle chiese più antiche, anticamente dedicata all'Ascensione, situata presso i resti del castello. Nel monastero annesso fu educanda la zia paterna Giovanna Verga Catalano (Mamma Vanna). \r\n\r\n<b>Riferimenti letterari:</b> «Donna Giovanna... era stata educata a Santa Maria dei Greci...» (Federico De Roberto, Casa Verga). Il luogo è legato alla genesi di 'Storia di una Capinera' attraverso le lettere delle zie monache.",
                    'order': 4,
                    'tratteggiato': False
                },
                {
                    'nome': '5ª tappa - Via Santa Maria dei Greci',
                    'coords': [37.161150, 14.746500],
                    'descrizione_breve': 'Palazzo Trao-Ventimiglia e Casa di Mastro-don Gesualdo.',
                    'descrizione': "Include la Chiesa di Sant'Anna e il Collegio di Maria, istituto per l'educazione delle fanciulle con stucchi di Natale Bonajuto. Comprende la prima abitazione di Gesualdo Motta nel Vico Ventimiglia e il Palazzo Trao-Ventimiglia, dimora di Bianca Trao, che oggi ospita il Museo dell'Immaginario Verghiano con le fotocamere originali di Giovanni Verga. \r\n\r\n<b>Riferimenti letterari:</b> «Dal palazzo dei Trao... si vedevano salire infatti... globi di fumo denso, a ondate, sparsi di faville» (Mastro-don Gesualdo).",
                    'order': 5,
                    'tratteggiato': False
                },
                {
                    'nome': "6ª tappa - Scalazza di Sant'Agata",
                    'coords': [37.161092051605365, 14.748270523188657],
                    'descrizione_breve': "Chiesa di Sant'Agata, ricostruita dopo il 1693.",
                    'descrizione': "Edificata nel XIII secolo e ricostruita dopo il sisma del 1693. All'altar maggiore conserva la pala del Martirio di Sant'Agata (1620) di Giovanni Bonino. \r\n\r\n<b>Riferimenti letterari:</b> «Il sole di sesta scappava dalle cortine... e faceva rifiorire le piaghe di sant'Agata... quasi due grosse rose in mezzo al petto» (Mastro-don Gesualdo).",
                    'order': 6,
                    'tratteggiato': False
                },
                {
                    'nome': '7ª tappa - Via Roma / Vico Rinaldi',
                    'coords': [37.16197641415655, 14.75018500725533],
                    'descrizione_breve': "Antica Strada Maddalena, il Torrione e il Condotto.",
                    'descrizione': "È l'antica Strada Maddalena lungo la quale il patriziato edificò i propri palazzi dopo il 1693. Include la sopraelevata detta Torrione, progettata dall'architetto Francesco Fichera. È visibile il Condotto sotterraneo citato nel Mastro-don Gesualdo come via di fuga di don Diego Trao. \r\n\r\n<b>Riferimenti letterari:</b> «Ciolla... vide ancora fermi sotto il voltone del Condotto, malgrado il gran puzzo, quasi al buio...» (Mastro-don Gesualdo).",
                    'order': 7,
                    'tratteggiato': False
                },
                {
                    'nome': '8ª tappa - Via Volta',
                    'coords': [37.162468164816566, 14.749514680772105],
                    'descrizione_breve': 'Case di Santuzza e Lola nel quartiere Purgatorio.',
                    'descrizione': "Via dell'antico quartiere Purgatorio che conserva la fisionomia popolare ottocentesca. Qui sorgono le case delle due protagoniste della sfida rusticana. \r\n\r\n<b>Riferimenti letterari:</b> «Lola che ascoltava ogni sera, nascosta dietro il vaso di basilico... un giorno chiamò Turiddu» (Cavalleria Rusticana).",
                    'order': 8,
                    'tratteggiato': False
                },
                {
                    'nome': '9ª tappa - Piazzetta Santa Teresa',
                    'coords': [37.16174586655226, 14.748813159162806],
                    'descrizione_breve': 'Osteria della gna Nunzia e Monastero di Santa Teresa.',
                    'descrizione': "Luogo dell'Osteria della gna Nunzia, teatro del bacio della sfida tra Turiddu e Alfio. Include la Chiesa e il Monastero di Santa Teresa (già delle Anime del Purgatorio), che conserva gelosie monastiche e una Crocifissione di Ludovico Svirech. \r\n\r\n<b>Riferimenti letterari:</b> «Turiddu strinse fra i denti l'orecchio del carrettiere, e così gli fece promessa solenne di non mancare» (Cavalleria Rusticana).",
                    'order': 9,
                    'tratteggiato': False
                }
            ],
            'traduzioni': {
                'en': {
                    'titolo': '1st Verga Itinerary – Places, landscapes and memories',
                    'descrizione': 'Urban itinerary through the historic center of Vizzini, reconstructing the real and literary places of Giovanni Verga.'
                }
            }
        },
        {
            'titolo': 'Vizzini – 2° Itinerario: Formazione e Famiglia',
            'slug': 'itinerario-verghiano-vizzini-2',
            'descrizione': 'Itinerario di approfondimento biografico e familiare dedicato ai luoghi della formazione affettiva, culturale e spirituale di Giovanni Verga, con particolare riferimento alla giovinezza e ai rapporti familiari.',
            'tipo': 'verghiano',
            'ordine': 2,
            'durata_stimata': '1-2 ore',
            'difficolta': 'facile',
            'is_active': True,
            'link_maps': 'https://maps.app.goo.gl/H1xERotyRnKThN2y7',
            'colore_percorso': '#4A6741',
            'immagine_path': 'itinerari/vizzini-verga-2.jpg',
            'coordinate_tappe': [
                {
                    'nome': '1ª tappa - Piazza Umberto I',
                    'coords': [37.16144617637193, 14.748882339392699],
                    'descrizione_breve': 'Partenza dalla piazza centrale e Palazzo Verga-Catalano.',
                    'descrizione': "Punto di partenza dell'itinerario. Include Palazzo Verga-Catalano, dimora della famiglia dello scrittore riedificata a metà Ottocento, Palazzo Sganci e la tardo-barocca Casa Senatoria. Dirimpetto alla piazza si trovava il palazzo Catalano appartenuto alla famiglia della nonna paterna.",
                    'order': 1,
                    'tratteggiato': False
                },
                {
                    'nome': "2ª tappa - Circolo Culturale 'Giovanni Verga'",
                    'coords': [37.161486193598435, 14.74989024809321],
                    'descrizione_breve': 'Sede storica del Club di Vizzini frequentato dai Verga.',
                    'descrizione': "Originariamente denominato Club di Vizzini e sede dell'Associazione dei Nobili. Una lettera del 1874 di Mario Verga al fratello Pietro testimonia l'interesse della famiglia per l'arredamento del Circolo, curato con mobili acquistati a Catania. \r\n\r\n<b>Documenti:</b> «Riceverai la presente da due carrettieri... per cominciare e rilevare quei mobili che sono pronti in istante di partire».",
                    'order': 2,
                    'tratteggiato': False
                },
                {
                    'nome': '3ª tappa - Chiesa e Monastero di San Sebastiano',
                    'coords': [37.161641676370806, 14.752334993871623],
                    'descrizione_breve': 'Luogo della zia monaca e suggestione per Storia di una Capinera.',
                    'descrizione': "Chiesa riedificata dopo il 1693 in stile rococò con affreschi dell'Antico Testamento. Il giovane Verga la frequentava per visitare la zia monaca Suor Carmela (Donna Rosalia Verga). L'incontro con l'educanda Agatina Passanisi costituì la suggestione per 'Storia di una Capinera'. \r\n\r\n<b>Testimonianze:</b> «...andando a visitarla nel parlatoio egli scorgeva il profilo della educanda» (Federico De Roberto).",
                    'order': 3,
                    'tratteggiato': False
                },
                {
                    'nome': '4ª tappa - Palazzo La Gurna',
                    'coords': [37.162051362082, 14.752741513396394],
                    'descrizione_breve': 'Banchetto nuziale di Mastro-don Gesualdo.',
                    'descrizione': "Edificio settecentesco caratterizzato da un prospetto con due colonne su alte basi in pietra vulcanica. Verga vi ambienta il banchetto nuziale tra Gesualdo Motta e Bianca Trao. \r\n\r\n<b>Riferimenti letterari:</b> «Nella casa antica dei La Gurna, presa in affitto da don Gesualdo Motta, s'aspettavano gli sposi» (Mastro-don Gesualdo).",
                    'order': 4,
                    'tratteggiato': False
                },
                {
                    'nome': '5ª tappa - Piazza Guglielmo Marconi',
                    'coords': [37.16229382618039, 14.753720991201575],
                    'descrizione_breve': 'Basilica monumentale di San Giovanni Battista.',
                    'descrizione': "Realizzata su progetto di Giovan Battista Giarrusso e ultimata nel 1743 (facciata di Francesco Viola). L'interno è arricchito da stucchi di Antonino Bonajuto e dal gruppo dell'Addolorata (1720). \r\n\r\n<b>Riferimenti letterari:</b> «Laggiù, verso la valle, la campana di San Giovanni suonava la messa grande... Viva San Giovanni!» (Jeli il pastore).",
                    'order': 5,
                    'tratteggiato': False
                },
                {
                    'nome': '6ª tappa - Via Roma / Vico Rinaldi',
                    'coords': [37.16197641415655, 14.75018500725533],
                    'descrizione_breve': "Antica Strada Maddalena e il Torrione.",
                    'descrizione': "Antica via sede dei palazzi patrizi dopo il 1693. Include la sopraelevata detta Torrione (arch. Fichera) e il Condotto imboccato da don Diego Trao per recarsi dalla cugina Baronessa Rubiera.",
                    'order': 6,
                    'tratteggiato': False
                }
            ],
            'traduzioni': {
                'en': {
                    'titolo': '2nd Verga Itinerary – Biography and Family',
                    'descrizione': 'Itinerary dedicated to the emotional and cultural formation of Giovanni Verga.'
                }
            }
        },
        {
            'titolo': 'Licodia Eubea – Luoghi, paesaggi e memorie',
            'slug': 'itinerario-verghiano-licodia-eubea',
            'descrizione': 'Percorso urbano e paesaggistico che attraversa il centro storico di Licodia Eubea, mettendo in relazione architetture, archivi e tradizioni locali con le opere e la produzione fotografica di Giovanni Verga.',
            'tipo': 'verghiano',
            'ordine': 3,
            'durata_stimata': '2 ore',
            'difficolta': 'facile',
            'is_active': True,
            'link_maps': 'https://maps.app.goo.gl/RRdbLWzfwoNP6Vxz6',
            'colore_percorso': '#008080',
            'immagine_path': 'itinerari/licodia-verga.jpg',
            'coordinate_tappe': [
                {
                    'nome': '1. Chiesa del Crocifisso (o della Trinità)',
                    'coords': [37.15625221315362, 14.703384301588802],
                    'descrizione_breve': "Chiesa seicentesca legata al fondo 'Giardino del Barone'.",
                    'descrizione': "Corso Umberto I, 212. Caratterizzata da una facciata dorica monumentale e volta decorata dalle Sette Opere di Misericordia. Legata al 'Giardino del Barone', fondo rustico acquistato dal nonno Giovanni Carmelo Verga Distefano con vigneti, favate, pascoli e ristoppie. La processione del Cristo Portacroce trascinato da Circello è descritta da Verga in una lettera del 1896.",
                    'order': 1,
                    'tratteggiato': False
                },
                {
                    'nome': '2. Piazza Garibaldi - Corso Umberto I',
                    'coords': [37.1558551782907, 14.70283480226759],
                    'descrizione_breve': "L'antica 'Strata Longa' fotografata dallo scrittore.",
                    'descrizione': "Già via del Casino o 'A strata longa'. Tratto urbano fotografato da Verga nel giugno 1897; il documento nota l'assenza, all'epoca, della liberty casa Agnello visibile oggi sulla destra.",
                    'order': 2,
                    'tratteggiato': False
                },
                {
                    'nome': "3. Sede Archeoclub d'Italia",
                    'coords': [37.15563694887419, 14.702283726960289],
                    'descrizione_breve': 'Collezione verghiana e ritratto dello zio Salvatore.',
                    'descrizione': "Corso Umberto I, 232. Conserva edizioni illustrate, il ritratto a olio dello zio Salvatore Verga Catalano e una foto originale dello scrittore scattata a Venezia (ante 1889) presso l'atelier Fratelli Vianelli.",
                    'order': 3,
                    'tratteggiato': False
                },
                {
                    'nome': '4. Chiesa del Carmine - Mausoleo Interlandi-Ottolini',
                    'coords': [37.15691804727959, 14.70147215948241],
                    'descrizione_breve': 'Monumenti funerari degli antenati Ottolini.',
                    'descrizione': "Piazza Giovanni XXIII. Contiene i monumenti marmorei dei baroni Interlandi. Gli Ottolini, antenati dello scrittore tramite Grazia Strazzuso Bertone, sono documentati qui dal Cinquecento al servizio dei Principi di Butera. \r\n\r\n<b>Bibliografia:</b> Mugnos (1670) cita Giovanni Ottolini Viviani come procuratore generale ai servigi di D. Francesco Santapau.",
                    'order': 4,
                    'tratteggiato': False
                },
                {
                    'nome': '5. Chiesa Madre di Santa Margherita',
                    'coords': [37.15502654470104, 14.700106756360942],
                    'descrizione_breve': 'Chiesa basilicale citata in Jeli e L\'amante di Gramigna.',
                    'descrizione': "Piazza Vittorio Emanuele II. Chiesa a tre navate con campanile accostato all'abside. \r\n\r\n<b>Riferimenti letterari:</b> «Peppa... portava lo stendardo di Santa Margherita come fosse un pilastro...» (L'amante di Gramigna); «Jeli insegnava... ad arrampicarsi... sui noci più alti del campanile di Licodia» (Jeli il pastore).",
                    'order': 5,
                    'tratteggiato': False
                },
                {
                    'nome': '6. Viale Calcide - Belvedere di Tebidi',
                    'coords': [37.15385645658828, 14.69772347278799],
                    'descrizione_breve': 'Punto panoramico sulla tenuta verghiana di Tebidi.',
                    'descrizione': "Belvedere sulla tenuta di Tebidi, dove Verga villeggiava. Legato a Jeli il pastore, Mastro-don Gesualdo e Storia di una Capinera (incontro con l'educanda vizzinese durante il colera). Si dice sia il luogo natale dello scrittore.",
                    'order': 6,
                    'tratteggiato': False
                },
                {
                    'nome': '7. Castello Santapau',
                    'coords': [37.153863540084124, 14.698642309128832],
                    'descrizione_breve': "Rovine dell'antica acropoli di Licodia.",
                    'descrizione': "Rilievo calcarenitico con rovine bizantine e normanne, distrutto nel 1693. Verga ne fotografò i ruderi nel 1897. Gli Ottolini furono al servizio dei principi Santapau nel XVI secolo.",
                    'order': 7,
                    'tratteggiato': False
                },
                {
                    'nome': '8. Ex Badia di San Benedetto e Santa Chiara',
                    'coords': [37.15530106075149, 14.7012202247638],
                    'descrizione_breve': "Antica Agenzia dei Tabacchi e 'ruota dei proietti'.",
                    'descrizione': "Piazza Stefania Noce. Agenzia dei Tabacchi dello Stato dopo il 1866. Qui fu abbandonata Gregoria Calogera Fortunata Verga (Lidda), figlia naturale dello zio Salvatore e di una contadina di Tebidi. \r\n\r\n<b>Riferimenti letterari:</b> «...fra Serafino col tabacco buono di Licodia...» (Papa Sisto).",
                    'order': 8,
                    'tratteggiato': False
                }
            ],
            'traduzioni': {
                'en': {
                    'titolo': 'Licodia Eubea – Places, landscapes and memories',
                    'descrizione': 'Urban and landscape route exploring the connections between Licodia Eubea and Giovanni Verga.'
                }
            }
        },
        {
            'titolo': 'Mineo – Itinerario Capuaniano',
            'slug': 'itinerario-capuaniano-mineo',
            'descrizione': 'Itinerario urbano che attraversa il centro storico di Mineo, ricostruendo i luoghi legati alla vita e alle opere di Luigi Capuana.',
            'tipo': 'capuaniano',
            'ordine': 1,
            'durata_stimata': '3-4 ore',
            'difficolta': 'facile',
            'is_active': True,
            'link_maps': 'https://maps.app.goo.gl/AcVAhkJwpEs6xoBU9',
            'colore_percorso': '#8B4513',
            'immagine_path': 'itinerari/mineo-capuana.jpg',
            'coordinate_tappe': [
                {
                    'nome': '1ª tappa - Porta Adinolfo (Porta Vecchia)',
                    'coords': [37.2652002259367, 14.69198789706867],
                    'descrizione_breve': "Antica porta dedicata all'eroe locale dei Vespri.",
                    'descrizione': "Una delle quattro antiche porte murate. \r\n\r\n<b>Riferimenti letterari:</b> «Usciti fuori Porta Vecchia, infilavano il gran viale alberato a passi gravi e lenti...» (La casa nuova); citata anche in Zi' Gamella e Don Peppantonio.",
                    'order': 1,
                    'tratteggiato': False
                },
                {
                    'nome': '2ª tappa - Piazza dei Vespri',
                    'coords': [37.26509009273927, 14.691507466767927],
                    'descrizione_breve': 'Piazzetta delle Orfanelle e l\'arresto del Marchese.',
                    'descrizione': "Nota come Piazzetta delle Orfanelle. \r\n\r\n<b>Riferimenti letterari:</b> «I carabinieri sono andati ad arrestarlo. Guardate, là, nella Piazzetta delle Orfanelle...» (Il Marchese di Roccaverdina); citata anche ne Le Verginelle.",
                    'order': 2,
                    'tratteggiato': False
                },
                {
                    'nome': '3ª tappa - Piazza Buglio',
                    'coords': [37.26515706449341, 14.691070510560824],
                    'descrizione_breve': 'Piazza centrale con statua bronzea di Luigi Capuana.',
                    'descrizione': "Ex Piazza del Mercato o dell'Orologio. Ospita la statua bronzea di Capuana realizzata da Vincenzo Torre (1936). \r\n\r\n<b>Riferimenti letterari:</b> «Pareva la festa di Sant'Isidoro. Gran folla in Piazza del Mercato attorno ai partenti» (Gli 'americani' di Rabbato); citata anche ne Il Marchese di Roccaverdina.",
                    'order': 3,
                    'tratteggiato': False
                },
                {
                    'nome': '4ª tappa - Palazzo Comunale',
                    'coords': [37.26488284665568, 14.691101893752075],
                    'descrizione_breve': 'Ex Collegio Gesuitico costruito nel 1588.',
                    'descrizione': "Sede comunale dal 1841. \r\n\r\n<b>Riferimenti letterari:</b> «...e, di rimpetto al Casino, il portone della Casa comunale, un ex convento, coi gradini affollati di oziosi...» (Bagni di sole).",
                    'order': 4,
                    'tratteggiato': False
                },
                {
                    'nome': '5ª tappa - Chiesa del Collegio (S. Tommaso Apostolo)',
                    'coords': [37.26479746721268, 14.690912220953734],
                    'descrizione_breve': 'Edificio del 1595 con opere di Filippo Paladini.',
                    'descrizione': "Presenta paliotti in marmo mischio settecenteschi e la Deposizione (1613) di Filippo Paladini. \r\n\r\n<b>Riferimenti letterari:</b> «E sugli scalini del Collegio... si vedeva tutti i giorni lo zi' Carmine, il tavernaio...» (Lo sciancato).",
                    'order': 5,
                    'tratteggiato': False
                },
                {
                    'nome': '6ª tappa - Monastero di San Benedetto',
                    'coords': [37.264518284908974, 14.689265480557665],
                    'descrizione_breve': 'Monastero Vecchio e l\'abbandono dei neonati.',
                    'descrizione': "Noto come Monastero Vecchio, luogo della 'ruota dei proietti'. \r\n\r\n<b>Riferimenti letterari:</b> «E questa povera creatura non sarebbe stata buttata... dietro la porta grande del Monastero Vecchio...» (Don Peppantonio); citata anche in Donna Straula.",
                    'order': 6,
                    'tratteggiato': False
                },
                {
                    'nome': '7ª tappa - Chiesa di Santa Agrippina',
                    'coords': [37.264737470504286, 14.688399609095926],
                    'descrizione_breve': 'Chiesa Matrice con statua di Vincenzo Archifel.',
                    'descrizione': "Fondata nei primi secoli della Cristianità, è Matrice dal 1582. Custodisce la statua della patrona (1518) di Vincenzo Archifel. \r\n\r\n<b>Riferimenti letterari:</b> «La domenica dell'ottavario però vedeva lassù... la bara di santa Agrippina portata dai devoti...» (Scurpiddu).",
                    'order': 7,
                    'tratteggiato': False
                },
                {
                    'nome': '8ª tappa - Circolo di Cultura',
                    'coords': [37.26546666386141, 14.690959452888821],
                    'descrizione_breve': 'L\'antico Casino dei Nobili di Bagni di sole.',
                    'descrizione': "Antico carcere e casino dei civili. \r\n\r\n<b>Riferimenti letterari:</b> «Gli associati fanno parte della mobilia del Casino. Stanno lì con la stessa immobilità del divano...» (Bagni di sole); citata anche in Il Benefattore.",
                    'order': 8,
                    'tratteggiato': False
                },
                {
                    'nome': '9ª tappa - Chiesa di San Pietro',
                    'coords': [37.26665309974458, 14.68997858172483],
                    'descrizione_breve': 'Chiesa barocca e la Maricchia de Lo sciancato.',
                    'descrizione': "Facciata concava barocca post-1693, conserva il Cristo alla colonna e arredi rococò. \r\n\r\n<b>Riferimenti letterari:</b> «— Meritava che io facessi come Maricchia che se lo spolpa vivo vivo...» (Lo sciancato).",
                    'order': 9,
                    'tratteggiato': False
                },
                {
                    'nome': '10ª tappa - Casa Capuana',
                    'coords': [37.26674831664237, 14.690839452888854],
                    'descrizione_breve': 'Palazzo natale e sede del Museo Capuaniano.',
                    'descrizione': "Palazzo borghese del XIX secolo. Sede della Biblioteca e del Museo capuaniano con i manoscritti e i cimeli dello scrittore. \r\n\r\n<b>Riferimenti letterari:</b> «Allora la nostra casa era molto diversa dalla palazzina che ora torreggia...» (Ricordi d'infanzia).",
                    'order': 10,
                    'tratteggiato': False
                },
                {
                    'nome': '11ª tappa - Chiesa di Santa Maria Maggiore',
                    'coords': [37.267292127782376, 14.692539810560799],
                    'descrizione_breve': 'Chiesa citata in Scurpiddu ed Evoluzione.',
                    'descrizione': "Conserva opere dal Rinascimento al Rococò. \r\n\r\n<b>Riferimenti letterari:</b> «Ma bisognava aspettare fino alla mezzanotte...» (Scurpiddu); citata anche in Evoluzione.",
                    'order': 11,
                    'tratteggiato': False
                },
                {
                    'nome': '12ª tappa - Castello Ducezio',
                    'coords': [37.268131215367504, 14.692704853276679],
                    'descrizione_breve': 'Torre ottagonale e passeggiata del Marchese.',
                    'descrizione': "Rovine dell'acropoli del V sec. a.C. con torre centrale ottagonale quasi intatta. \r\n\r\n<b>Riferimenti letterari:</b> «Unico svago del marchese era la passeggiata, lassù, su la spianata del Castello...» (Il Marchese di Roccaverdina).",
                    'order': 12,
                    'tratteggiato': False
                },
                {
                    'nome': '13ª tappa - Palazzo Morgana (Casa Roccaverdina)',
                    'coords': [37.26691631400821, 14.692453839396835],
                    'descrizione_breve': 'Ispirazione reale per la casa di Roccaverdina.',
                    'descrizione': "Palazzo della famiglia Buglio ricostruito dal barone Morgana dopo il 1693 utilizzando materiali di spoglio del Castello. \r\n\r\n<b>Riferimenti letterari:</b> «Dalla parte del viale che conduceva lassù, la casa dei Roccaverdina aveva l'entrata a pianterreno...» (Il Marchese di Roccaverdina).",
                    'order': 13,
                    'tratteggiato': False
                },
                {
                    'nome': '14ª tappa - Chiesa di San Francesco',
                    'coords': [37.26561529208114, 14.691246748864167],
                    'descrizione_breve': 'Portale quattrocentesco e novella Quacquarà.',
                    'descrizione': "Ex convento dei Minori, conserva statue lignee e tele settecentesche e un pregevole portale del XV secolo. \r\n\r\n<b>Riferimenti letterari:</b> «La mattina, spazzolato ben bene il vestito spelato e rattoppato...» (Quacquarà).",
                    'order': 14,
                    'tratteggiato': False
                },
                {
                    'nome': '15ª tappa - Chiesa della Madonna della Mercede',
                    'coords': [37.26507508453964, 14.691053837749353],
                    'descrizione_breve': 'Collegio di Maria e don Saverio de Il mago.',
                    'descrizione': "Chiesa annessa al Collegio di Maria. \r\n\r\n<b>Riferimenti letterari:</b> «Per questo, ogni sera, all'ora della benedizione, don Saverio si metteva a suonare il campanello...» (Il mago); citata anche in Un cronista e Don Peppantonio.",
                    'order': 15,
                    'tratteggiato': False
                }
            ],
            'traduzioni': {
                'en': {
                    'titolo': 'Mineo – Capuana Itinerary',
                    'descrizione': 'Urban route exploring the real and narrative places of Luigi Capuana in Mineo.'
                }
            }
        },
    ]
    
    for itinerario_data in itinerari_data:
        itinerario, created = Itinerario.objects.get_or_create(
            slug=itinerario_data['slug'],
            defaults={
                'tipo': itinerario_data.get('tipo', 'verghiano'),
                'ordine': itinerario_data.get('ordine', 1),
                'durata_stimata': itinerario_data.get('durata_stimata', ''),
                'difficolta': itinerario_data.get('difficolta', 'facile'),
                'link_maps': itinerario_data.get('link_maps', ''),
                'is_active': itinerario_data.get('is_active', True),
                'coordinate_tappe': itinerario_data.get('coordinate_tappe', []),
                'colore_percorso': itinerario_data.get('colore_percorso', '#4A6741'),
            }
        )
        
        if not created:
            itinerario.tipo = itinerario_data.get('tipo', 'verghiano')
            itinerario.ordine = itinerario_data.get('ordine', 1)
            itinerario.durata_stimata = itinerario_data.get('durata_stimata', '')
            itinerario.difficolta = itinerario_data.get('difficolta', 'facile')
            itinerario.link_maps = itinerario_data.get('link_maps', '')
            itinerario.is_active = itinerario_data.get('is_active', True)
            itinerario.coordinate_tappe = itinerario_data.get('coordinate_tappe', [])
            itinerario.colore_percorso = itinerario_data.get('colore_percorso', '#4A6741')
        
        # Copia l'immagine se specificata e non esiste già
        if 'immagine_path' in itinerario_data and itinerario_data['immagine_path'] and not itinerario.immagine:
            image_path = copy_static_to_media(
                itinerario_data['immagine_path'], 
                f"itinerari/{itinerario_data['slug']}.jpg"
            )
            if image_path:
                try:
                    media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    with open(media_path, 'rb') as f:
                        itinerario.immagine.save(f"{itinerario_data['slug']}.jpg", File(f), save=False)
                except Exception as e:
                    print(f"  ⚠️  Errore salvataggio immagine itinerario {itinerario_data['slug']}: {e}")
        
        # Imposta i campi traducibili italiano
        itinerario.set_current_language('it')
        itinerario.titolo = itinerario_data['titolo']
        itinerario.descrizione = itinerario_data['descrizione']
        itinerario.save()
        
        # Imposta traduzioni inglese se disponibili
        if 'traduzioni' in itinerario_data and 'en' in itinerario_data['traduzioni']:
            itinerario.set_current_language('en')
            itinerario.titolo = itinerario_data['traduzioni']['en']['titolo']
            itinerario.descrizione = itinerario_data['traduzioni']['en']['descrizione']
            itinerario.save()
        
        if created:
            print(f"✓ Creato itinerario: {itinerario_data['titolo']}")
        else:
            print(f"• Itinerario aggiornato: {itinerario_data['titolo']}")
    
    # Riepilogo finale
    print("\n" + "="*70)
    print("POPOLAMENTO ITINERARI COMPLETATO!")
    print("="*70)
    print(f"\nTotale itinerari: {Itinerario.objects.count()}")
    print(f"  - Itinerari verghiani: {Itinerario.objects.filter(tipo='verghiano').count()}")
    print(f"  - Itinerari capuaniani: {Itinerario.objects.filter(tipo='capuaniano').count()}")
    print(f"  - Itinerari tematici: {Itinerario.objects.filter(tipo='tematico').count()}")


if __name__ == '__main__':
    populate_itinerari()
