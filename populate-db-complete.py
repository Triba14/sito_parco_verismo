#!/usr/bin/env python3
"""
Script completo per popolare e gestire il database del Parco Letterario Giovanni Verga e Luigi Capuana.
Include:
- Popolamento database (autori, opere, eventi, notizie, archivio foto, itinerari)
- Creazione superuser
- Aggiornamento coordinate itinerari per mappa interattiva
- Verifica e controllo dati

Esegui con: 
  python populate_db_complete.py                    # Popola database completo
  python populate_db_complete.py --create-superuser # Crea solo superuser
  python populate_db_complete.py --update-coords    # Aggiorna coordinate itinerari
  python populate_db_complete.py --check            # Verifica dati
"""
import os
import django
from datetime import datetime, timedelta
from django.core.files import File
import shutil
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Autore, Opera, Evento, Notizia, FotoArchivio, Itinerario
from django.conf import settings
from django.contrib.auth import get_user_model

def create_superuser():
    """
    Crea il superuser admin con password admin123 SOLO se non esiste.
    Se esiste già, non tocca la password.
    """
    User = get_user_model()
    username = 'admin'
    email = 'admin@parcolettverismo.it'
    password = 'admin123'
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_staff': True, 'is_superuser': True}
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✓ Superuser creato: {username} / {password}")
    else:
        # Non aggiornare la password se l'utente esiste già!
        print(f"• Superuser già esistente: {username} (password non modificata)")

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

def populate():
    print("="*70)
    print("POPOLAMENTO COMPLETO DEL DATABASE")
    print("="*70)
    
    # ========================================================================
    # CREAZIONE SUPERUSER
    # ========================================================================
    print("\n" + "="*70)
    print("CREAZIONE SUPERUSER")
    print("="*70)
    create_superuser()
    
    # ========================================================================
    # CREAZIONE AUTORI
    # ========================================================================
    print("\n" + "="*70)
    print("CREAZIONE AUTORI")
    print("="*70)
    
    verga, created = Autore.objects.get_or_create(
        slug='giovanni-verga',
        defaults={'nome': 'Giovanni Verga'}
    )
    if created:
        print(f"✓ Creato autore: {verga.nome}")
    else:
        print(f"• Autore già esistente: {verga.nome}")
    
    capuana, created = Autore.objects.get_or_create(
        slug='luigi-capuana',
        defaults={'nome': 'Luigi Capuana'}
    )
    if created:
        print(f"✓ Creato autore: {capuana.nome}")
    else:
        print(f"• Autore già esistente: {capuana.nome}")
    
    # ========================================================================
    # OPERE DI GIOVANNI VERGA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI GIOVANNI VERGA")
    print("="*70)
    
    opere_verga = [
        {
            'titolo': 'Mastro-don Gesualdo',
            'slug': 'mastro-don-gesualdo',
            'anno_pubblicazione': 1889,
            'breve_descrizione': 'Secondo romanzo del Ciclo dei Vinti di Verga, incentrato sull\'ascesa sociale e il fallimento esistenziale di un self-made man siciliano nell\'Ottocento.',
            'trama': 'Gesualdo Motta è un muratore che attraverso il lavoro instancabile e l\'astuzia accumula ricchezze, diventando uno dei più potenti proprietari terrieri di Vizzini. Per consolidare la sua posizione sociale sposa Bianca Trao, nobile decaduta. Tuttavia, il matrimonio è un disastro: Bianca lo disprezza per le sue origini umili, la figlia Isabelle si vergogna di lui, e la nobiltà locale non lo accetta mai veramente. Gesualdo resta intrappolato tra due mondi: troppo ricco per i poveri, troppo plebeo per i nobili. Malato e solo, muore nel palazzo palermitano della figlia, circondato dall\'indifferenza e dal disgusto dei servi, che lo vedono solo come un intruso.',
            'analisi': 'Il romanzo esplora il tema della "roba" (il possesso materiale) come ossessione e condanna. Gesualdo conquista tutto ma perde sé stesso: la sua vittoria economica coincide con la sua disfatta umana. Verga mostra come la mobilità sociale sia illusoria in una società rigidamente stratificata, e come l\'ambizione possa diventare una forma di autodistruzione. La solitudine finale del protagonista rappresenta il prezzo della violazione delle leggi implicite della società siciliana ottocentesca.',
            'link_wikisource': ' https://it.wikisource.org/wiki/Mastro-don_Gesualdo_(1889)',
            'copertina_path': 'storia_di_una_capinera.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Mastro-don Gesualdo',
                    'breve_descrizione': 'Second novel of Verga\'s Cycle of the Vanquished, focused on the social rise and existential failure of a Sicilian self-made man in the 19th century.',
                    'trama': 'Gesualdo Motta is a mason who, through tireless work and cunning, accumulates wealth, becoming one of the most powerful landowners in Vizzini. To consolidate his social position, he marries Bianca Trao, a declining noblewoman. However, the marriage is a disaster: Bianca despises him for his humble origins, his daughter Isabella is ashamed of him, and the local nobility never truly accepts him. Gesualdo remains trapped between two worlds: too rich for the poor, too plebeian for the nobles. Sick and alone, he dies in his daughter\'s Palermo palace, surrounded by the indifference and disgust of servants who see him only as an intruder.',
                    'analisi': 'The novel explores the theme of "roba" (material possession) as both obsession and condemnation. Gesualdo conquers everything but loses himself: his economic victory coincides with his human defeat. Verga shows how social mobility is illusory in a rigidly stratified society, and how ambition can become a form of self-destruction. The protagonist\'s final solitude represents the price of violating the implicit laws of 19th-century Sicilian society.'
                }
            }
        },
        {
            'titolo': 'Storia di una capinera',
            'slug': 'storia-di-una-capinera',
            'anno_pubblicazione': 1871,
            'breve_descrizione': 'Romanzo epistolare che racconta il dramma di una vocazione religiosa imposta e il conflitto tra desiderio individuale e costrizione sociale.',
            'trama': 'Maria è una giovane educanda cresciuta in convento fin dall’infanzia, destinata alla vita monastica senza aver mai potuto scegliere. A causa di un’epidemia, viene temporaneamente accolta nella casa di famiglia, dove entra per la prima volta in contatto con il mondo esterno: la natura, la vita domestica, gli affetti e soprattutto l’amore, incarnato dalla figura di Nino. Questo breve periodo di libertà apre una frattura irreversibile nella sua interiorità. Quando Maria è costretta a rientrare in convento, la separazione dal mondo e dall’amore la conduce a una progressiva disgregazione psicologica, fino alla follia e alla morte spirituale.',
            'analisi': 'Pur appartenendo alla fase pre-verista, il romanzo anticipa temi centrali dell’opera di Verga: l’impossibilità di sottrarsi al destino sociale, la violenza silenziosa delle istituzioni e il sacrificio dell’individuo in nome dell’ordine collettivo. La forma epistolare accentua l’isolamento della protagonista e rende evidente la distanza tra mondo interno e realtà esterna.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Storia_di_una_capinera',
            'copertina_path': 'storia_di_una_capinera.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Storia di una capinera',
                    'breve_descrizione': 'Epistolary novel that tells the drama of an imposed religious vocation and the conflict between individual desire and social constraint.',
                    'trama': 'Maria is a young boarder raised in a convent since childhood, destined for monastic life without ever being able to choose. Due to an epidemic, she is temporarily welcomed into her family home, where she comes into contact with the external world for the first time: nature, domestic life, affection, and especially love, embodied by Nino. This brief period of freedom opens an irreversible fracture in her interiority. When Maria is forced to return to the convent, the separation from the world and from love leads her to a progressive psychological disintegration, culminating in madness and spiritual death.',
                    'analisi': 'Although belonging to the pre-verismo phase, the novel anticipates central themes of Verga\'s work: the impossibility of escaping social destiny, the silent violence of institutions, and the sacrifice of the individual in the name of collective order. The epistolary form accentuates the protagonist\'s isolation and makes evident the distance between internal world and external reality.'
                }
            }
        },
        {
            'titolo': 'Nedda',
            'slug': 'nedda',
            'anno_pubblicazione': 1874,
            'breve_descrizione': 'Novella che racconta la vita di una giovane contadina, segnata dalla miseria, dal lavoro stagionale e dalla perdita degli affetti.',
            'trama': 'Nedda è una raccoglitrice di olive che vive in condizioni di estrema povertà insieme alla madre malata. La sua esistenza è scandita dal lavoro duro, dalla precarietà e dall’assenza di prospettive. L’unico spiraglio di felicità è l’amore per Janu, un giovane bracciante con cui sogna una vita diversa. Ma la malattia, la morte e l’indifferenza sociale si abbattono su di lei senza tregua, privandola anche di questa speranza. Rimasta sola, Nedda affronta la vita con una dignità silenziosa, accettando un destino che non concede redenzione.',
            'analisi': 'Nedda è un testo di passaggio verso il Verismo maturo. Verga rinuncia a qualsiasi idealizzazione e osserva la miseria come una condizione strutturale. Il dolore non è eccezionale, ma quotidiano; la tragedia non è spettacolare, ma sommessa e continua.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Nedda',
            'copertina_path': 'nedda.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Nedda',
                    'breve_descrizione': 'Novella that tells the life of a young peasant woman, marked by poverty, seasonal labor, and the loss of affection.',
                    'trama': 'Nedda is an olive picker who lives in extreme poverty with her sick mother. Her existence is marked by hard work, precariousness, and lack of prospects. The only glimmer of happiness is her love for Janu, a young farmhand with whom she dreams of a different life. But illness, death, and social indifference strike her relentlessly, depriving her even of this hope. Left alone, Nedda faces life with silent dignity, accepting a destiny that offers no redemption.',
                    'analisi': 'Nedda is a transitional text towards mature Verismo. Verga renounces any idealization and observes poverty as a structural condition. Pain is not exceptional but daily; tragedy is not spectacular but subdued and continuous.'
                }
            }
        },
        {
            'titolo': 'Fantasticheria',
            'slug': 'fantasticheria',
            'anno_pubblicazione': 1880,
            'breve_descrizione': 'Racconto-manifesto che esplicita il metodo narrativo verghiano e il suo sguardo sugli “umili”.',
            'trama': 'Il narratore si rivolge a una donna dell’alta società che, durante un soggiorno in un villaggio di pescatori, ha osservato quella vita semplice con curiosità superficiale e distacco. Verga smonta questa visione romantica, mostrando come dietro l’apparente immobilità si nascondano equilibri fragili, sacrifici, rinunce e una feroce lotta per la sopravvivenza. Il racconto non segue una vera azione narrativa, ma è costruito come una riflessione sulla distanza tra chi guarda e chi vive realmente quella realtà.',
            'analisi': 'Fantasticheria è fondamentale per comprendere il Verismo: Verga rifiuta la compassione estetizzante e invita a osservare la realtà popolare dall’interno, senza filtri morali o sentimentali. È una dichiarazione di poetica mascherata da racconto.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Fantasticheria',
            'copertina_path': 'fantasticheria.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Fantasticheria',
                    'breve_descrizione': 'Manifesto-story that explicates Verga\'s narrative method and his gaze on the "humble".',
                    'trama': 'The narrator addresses an upper-class woman who, during a stay in a fishing village, observed that simple life with superficial curiosity and detachment. Verga dismantles this romantic vision, showing how behind the apparent immobility lie fragile balances, sacrifices, renunciations, and a fierce struggle for survival. The story does not follow true narrative action but is constructed as a reflection on the distance between those who observe and those who truly live that reality.',
                    'analisi': 'Fantasticheria is fundamental to understanding Verismo: Verga rejects aestheticizing compassion and invites observation of popular reality from within, without moral or sentimental filters. It is a declaration of poetics disguised as a story.'
                }
            }
        },
        {
            'titolo': 'Rosso Malpelo',
            'slug': 'rosso-malpelo',
            'anno_pubblicazione': 1880,
            'breve_descrizione': 'Una delle novelle più celebri di Verga, incentrata sul lavoro minorile e sulla disumanizzazione sociale.',
            'trama': 'Malpelo è un ragazzo che lavora in una cava di sabbia. Il colore dei suoi capelli lo marchia come naturalmente cattivo agli occhi degli altri, giustificando ogni violenza subita. Dopo la morte del padre, anch’egli minatore, Malpelo cresce in un ambiente che non conosce compassione. L’unico legame umano è con Ranocchio, un ragazzo debole e malato, che però non riesce a salvarsi. Isolato, brutalizzato e privato di ogni affetto, Malpelo interiorizza l’odio del mondo fino a scomparire nel cuore della miniera.',
            'analisi': 'Qui il Verismo raggiunge una delle sue espressioni più crude: l’ambiente sociale non solo opprime l’individuo, ma lo plasma. La violenza non è denunciata apertamente, ma emerge come fatto normale e accettato, rendendo il racconto ancora più disturbante.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Rosso_Malpelo',
            'copertina_path': 'rosso_malpelo.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Rosso Malpelo',
                    'breve_descrizione': 'One of Verga\'s most celebrated novellas, focused on child labor and social dehumanization.',
                    'trama': 'Malpelo is a boy who works in a sand quarry. The color of his hair marks him as naturally evil in the eyes of others, justifying every violence he suffers. After his father\'s death, also a miner, Malpelo grows up in an environment that knows no compassion. The only human bond is with Ranocchio, a weak and sick boy, whom he cannot save. Isolated, brutalized, and deprived of all affection, Malpelo internalizes the world\'s hatred until he disappears into the heart of the mine.',
                    'analisi': 'Here Verismo reaches one of its crudest expressions: the social environment not only oppresses the individual but shapes him. Violence is not openly denounced but emerges as a normal and accepted fact, making the story even more disturbing.'
                }
            }
        },
        {
            'titolo': 'Cavalleria rusticana',
            'slug': 'cavalleria-rusticana',
            'anno_pubblicazione': 1880,
            'breve_descrizione': 'Novella tragica incentrata sull’onore, sulla gelosia e sulla legge non scritta della comunità.',
            'trama': 'Turiddu torna al paese dopo il servizio militare e scopre che la donna amata ha spostato un altro uomo. Ferito nell’orgoglio, intreccia una relazione con Lola, ormai moglie di Alfio, scatenando una catena di rivalità e sospetti. La relazione viene scoperta, l’onore è compromesso e la comunità pretende una riparazione. Il conflitto non può che concludersi con un duello mortale, accettato come inevitabile da tutti i personaggi.',
            'analisi': 'La tragedia non nasce dalle passioni individuali, ma dal codice sociale che le governa. In Cavalleria rusticana l’individuo è completamente assorbito dalla collettività: nessuna scelta è veramente libera, tutto è già deciso dalle regole dell’onore.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Cavalleria_rusticana',
            'copertina_path': 'cavalleria_rusticana.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Cavalleria rusticana',
                    'breve_descrizione': 'Tragic novella focused on honor, jealousy, and the unwritten law of the community.',
                    'trama': 'Turiddu returns to his village after military service and discovers that the woman he loved has married another man. Wounded in pride, he starts a relationship with Lola, now wife of Alfio, triggering a chain of rivalry and suspicion. The relationship is discovered, honor is compromised, and the community demands reparation. The conflict can only conclude with a mortal duel, accepted as inevitable by all characters.',
                    'analisi': 'The tragedy does not arise from individual passions but from the social code that governs them. In Cavalleria rusticana the individual is completely absorbed by the collectivity: no choice is truly free, everything is already decided by the rules of honor.'
                }
            }
        },
        {
            'titolo': 'La lupa',
            'slug': 'la-lupa',
            'anno_pubblicazione': 1880,
            'breve_descrizione': 'Novella sul desiderio femminile e sulla sua demonizzazione all’interno della società rurale.',
            'trama': 'Gnà Pina, soprannominata “la Lupa”, è una donna dominata da una passione irrefrenabile. Il suo desiderio per Nanni, un giovane contadino, la porta a manipolare la vita della figlia, costringendola a sposarlo pur di averlo vicino. La relazione proibita e ossessiva distrugge ogni equilibrio familiare e sociale, conducendo a un crescendo di tensione che sfocia nella violenza finale.',
            'analisi': 'Verga mette in scena una società che non ammette deviazioni dal ruolo imposto alle donne. Il desiderio femminile viene trasformato in colpa e punito. Non c’è giudizio morale esplicito, ma una rappresentazione spietata dei meccanismi sociali.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/La_lupa',
            'copertina_path': 'la_lupa.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'La lupa',
                    'breve_descrizione': 'Novella about female desire and its demonization within rural society.',
                    'trama': 'Gnà Pina, nicknamed "la Lupa" (the She-Wolf), is a woman dominated by irrepressible passion. Her desire for Nanni, a young peasant, leads her to manipulate her daughter\'s life, forcing her to marry him just to have him close. The forbidden and obsessive relationship destroys every family and social balance, leading to a crescendo of tension that results in final violence.',
                    'analisi': 'Verga stages a society that does not admit deviations from the role imposed on women. Female desire is transformed into guilt and punished. There is no explicit moral judgment, but a ruthless representation of social mechanisms.'
                }
            }
        },
        {
            'titolo': 'I Malavoglia',
            'slug': 'i-malavoglia',
            'anno_pubblicazione': 1881,
            'breve_descrizione': 'Il grande romanzo verista sulla famiglia, sul lavoro e sulla sconfitta dei “vinti”.',
            'trama': 'La famiglia Toscano vive ad Aci Trezza seguendo ritmi antichi e un equilibrio fragile. Un tentativo di miglioramento economico, l’acquisto a credito di un carico di lupini, innesca una serie di disgrazie: la morte di Bastianazzo, i debiti, la perdita della casa, l’emigrazione e la disgregazione del nucleo familiare. Ogni tentativo di riscatto fallisce, fino a un parziale e amaro ritorno all’ordine originario.',
            'analisi': 'È il primo romanzo del ciclo dei Vinti. Verga mostra come il progresso economico non liberi, ma distrugga gli equilibri tradizionali. La comunità giudica, isola e punisce chi tenta di uscire dal proprio ruolo.',
            'link_wikisource': 'https://it.wikisource.org/wiki/I_Malavoglia',
            'copertina_path': 'i_malavoglia.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'I Malavoglia',
                    'breve_descrizione': 'The great verismo novel about family, work, and the defeat of the "vanquished".',
                    'trama': 'The Toscano family lives in Aci Trezza following ancient rhythms and a fragile balance. An attempt at economic improvement, the purchase on credit of a cargo of lupins, triggers a series of misfortunes: Bastianazzo\'s death, debts, the loss of the house, emigration, and the disintegration of the family nucleus. Every attempt at redemption fails, until a partial and bitter return to the original order.',
                    'analisi': 'It is the first novel of the Cycle of the Vanquished. Verga shows how economic progress does not liberate but destroys traditional balances. The community judges, isolates, and punishes those who try to leave their role.'
                }
            }
        },
        {
            'titolo': 'La roba',
            'slug': 'la-roba',
            'anno_pubblicazione': 1883,
            'breve_descrizione': 'Novella emblematica sull’ossessione per il possesso materiale.',
            'trama': 'Mazzarò, contadino arricchito, dedica l’intera esistenza all’accumulo di terre e beni. La sua vita è totalmente assorbita dalla “roba”, che diventa misura del suo valore. Quando la vecchiaia gli rivela che non potrà portare nulla con sé, esplode in una furia disperata contro le sue stesse ricchezze.',
            'analisi': 'La ricchezza non emancipa ma divora. Verga mostra come l’economia determini l’identità e come il possesso diventi una prigione psicologica e sociale.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_rusticane/La_roba',
            'copertina_path': 'la_roba.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'La roba',
                    'breve_descrizione': 'Emblematic novella about the obsession with material possession.',
                    'trama': 'Mazzarò, an enriched peasant, dedicates his entire existence to accumulating land and goods. His life is totally absorbed by "roba" (property), which becomes the measure of his value. When old age reveals to him that he cannot take anything with him, he explodes in desperate fury against his own riches.',
                    'analisi': 'Wealth does not emancipate but devours. Verga shows how economy determines identity and how possession becomes a psychological and social prison.'
                }
            }
        },
        {
            'titolo': 'Libertà',
            'slug': 'liberta',
            'anno_pubblicazione': 1883,
            'breve_descrizione': 'Novella storica sulla violenza collettiva e sull’illusione dell’emancipazione.',
            'trama': 'Durante i moti del 1860, la popolazione insorge contro i notabili, convinta che la libertà significhi immediata giustizia sociale. La rivolta degenera in violenza indiscriminata e saccheggi. L’arrivo dell’esercito ristabilisce l’ordine con una repressione altrettanto brutale, lasciando intatte le disuguaglianze.',
            'analisi': 'Verga smonta il mito della rivoluzione: la libertà, se non accompagnata da reali trasformazioni sociali, resta una parola vuota. Il racconto è una delle analisi più lucide del fallimento delle utopie politiche.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_rusticane/Libert%C3%A0',
            'copertina_path': 'liberta.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Libertà',
                    'breve_descrizione': 'Historical novella about collective violence and the illusion of emancipation.',
                    'trama': 'During the uprisings of 1860, the population rises against the notables, convinced that liberty means immediate social justice. The revolt degenerates into indiscriminate violence and looting. The arrival of the army restores order with equally brutal repression, leaving inequalities intact.',
                    'analisi': 'Verga dismantles the myth of revolution: liberty, if not accompanied by real social transformations, remains an empty word. The story is one of the most lucid analyses of the failure of political utopias.'
                }
            }
        },
    ]
    
    for opera_data in opere_verga:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': verga,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = verga
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        
        # Copia la copertina se specificata e non esiste già
        if 'copertina_path' in opera_data and not opera.copertina:
            # Salva in media/copertine/opere_Verga/
            copertina_path = copy_static_to_media(opera_data['copertina_path'], f"copertine/opere_Verga/{opera_data['slug']}.jpg")
            if copertina_path:
                media_path = os.path.join(settings.MEDIA_ROOT, copertina_path)
                with open(media_path, 'rb') as f:
                    opera.copertina.save(f"{opera_data['slug']}.jpg", File(f), save=False)
        
        # Se non c'è copertina (o perché non specificata o perché il file non esiste), usa il placeholder
        if not opera.copertina:
            opera.copertina.name = 'copertine/opere_Verga/placeHolder_verga.jpeg'

        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.breve_descrizione = opera_data.get('breve_descrizione', '')
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        
        # Salva traduzioni inglesi se disponibili
        if 'traduzioni' in opera_data and 'en' in opera_data['traduzioni']:
            opera.set_current_language('en')
            opera.titolo = opera_data['traduzioni']['en']['titolo']
            opera.breve_descrizione = opera_data['traduzioni']['en'].get('breve_descrizione', '')
            opera.trama = opera_data['traduzioni']['en'].get('trama', '')
            opera.analisi = opera_data['traduzioni']['en'].get('analisi', '')
            opera.save()
        
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # OPERE DI LUIGI CAPUANA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI LUIGI CAPUANA")
    print("="*70)
    
    opere_capuana = [
        {
            'titolo': 'Giacinta',
            'slug': 'giacinta',
            'anno_pubblicazione': 1879,
            'breve_descrizione': 'Romanzo che esplora in modo innovativo la psicologia femminile, il trauma e il determinismo, ponendosi come uno dei testi fondativi del Verismo italiano.',
            'trama': 'Giacinta è una giovane donna segnata da un trauma infantile che ne condiziona profondamente la vita affettiva e sociale. Cresciuta in un ambiente borghese, tenta di costruire relazioni sentimentali stabili, ma ogni legame è compromesso dalla sua fragilità emotiva e da un senso di colpa radicato. L’amore, il matrimonio e la maternità non riescono a offrirle redenzione. La sua vicenda è un lento scivolare verso l’autodistruzione, osservato con occhio clinico e privo di compiacimento.',
            'analisi': 'Giacinta è uno dei primi romanzi italiani a confrontarsi apertamente con il tema del determinismo psicologico. Capuana, influenzato dal naturalismo francese, analizza il personaggio come “caso”, ma senza annullarne l’umanità. Il romanzo segna una svolta nella narrativa italiana per la centralità della psiche e per la rappresentazione di una femminilità non idealizzata.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Giacinta',
            'copertina_path': 'giacinta.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Giacinta',
                    'breve_descrizione': 'Novel that innovatively explores female psychology, trauma, and determinism, establishing itself as one of the foundational texts of Italian Verismo.',
                    'trama': 'Giacinta is a young woman marked by childhood trauma that profoundly conditions her affective and social life. Raised in a bourgeois environment, she attempts to build stable sentimental relationships, but every bond is compromised by her emotional fragility and deep-rooted sense of guilt. Love, marriage, and motherhood cannot offer her redemption. Her story is a slow slide toward self-destruction, observed with a clinical eye devoid of complacency.',
                    'analisi': 'Giacinta is one of the first Italian novels to openly confront the theme of psychological determinism. Capuana, influenced by French naturalism, analyzes the character as a "case," but without annulling her humanity. The novel marks a turning point in Italian narrative for its focus on the psyche and representation of non-idealized femininity.'
                }
            }
        },
        {
            'titolo': 'Il marchese di Roccaverdina',
            'slug': 'il-marchese-di-roccaverdina',
            'anno_pubblicazione': 1901,
            'breve_descrizione': 'Il capolavoro narrativo di Capuana, un romanzo sul delitto, sulla colpa e sulla disgregazione morale dell’individuo.',
            'trama': 'Il marchese di Roccaverdina uccide il suo fattore per gelosia, ma riesce a sottrarsi alla giustizia umana. Tuttavia, il crimine lo condanna a una pena più profonda: il tormento interiore. Ossessionato dal rimorso e dalla paura, il marchese precipita in un progressivo isolamento psicologico, mentre la comunità che lo circonda resta indifferente o ignara. La sua mente si popola di allucinazioni, sospetti e visioni, fino al crollo finale.',
            'analisi': 'Il romanzo rappresenta una sintesi altissima tra Verismo e indagine psicologica. Capuana dimostra che il vero tribunale non è quello sociale, ma quello interiore. La Sicilia rurale diventa lo sfondo immobile di un dramma mentale, anticipando tematiche della narrativa novecentesca e avvicinandosi a una forma di realismo psicologico estremamente moderno.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Il_marchese_di_Roccaverdina',
            'copertina_path': 'il_marchese_di_roccaverdina.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Il marchese di Roccaverdina',
                    'breve_descrizione': 'Capuana\'s narrative masterpiece, a novel about crime, guilt, and the individual\'s moral disintegration.',
                    'trama': 'The Marquis of Roccaverdina kills his steward out of jealousy but manages to escape human justice. However, the crime condemns him to a deeper punishment: inner torment. Obsessed by remorse and fear, the marquis plunges into progressive psychological isolation, while the surrounding community remains indifferent or unaware. His mind becomes populated with hallucinations, suspicions, and visions, until the final collapse.',
                    'analisi': 'The novel represents a supreme synthesis between Verismo and psychological investigation. Capuana demonstrates that the true tribunal is not the social one but the inner one. Rural Sicily becomes the immobile backdrop of a mental drama, anticipating twentieth-century narrative themes and approaching an extremely modern form of psychological realism.'
                }
            }
        },
        {
            'titolo': 'Le paesane',
            'slug': 'le-paesane',
            'anno_pubblicazione': 1894,
            'breve_descrizione': 'Raccolta di novelle dedicate al mondo femminile rurale, osservato con attenzione antropologica e linguistica.',
            'trama': 'Le protagoniste delle novelle sono donne dei paesi siciliani: contadine, mogli, giovani innamorate, figure marginali la cui vita è scandita da lavoro, matrimonio, maternità e sacrificio. Ogni racconto mette in scena un’esistenza compressa entro ruoli sociali rigidi, dove i sentimenti individuali entrano in conflitto con le aspettative della comunità. Le storie non cercano soluzioni, ma registrano destini.',
            'analisi': 'Capuana adotta uno sguardo verista che non giudica e non consola. La lingua si modella sul parlato, la struttura narrativa è essenziale. Le paesane costituisce un documento prezioso sulla condizione femminile nel mondo rurale siciliano e sull’interazione tra individuo e tradizione.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Le_paesane',
            'copertina_path': 'le_paesane.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Le paesane',
                    'breve_descrizione': 'Collection of novellas dedicated to the rural female world, observed with anthropological and linguistic attention.',
                    'trama': 'The protagonists of the novellas are women from Sicilian villages: peasants, wives, young lovers, marginal figures whose lives are marked by work, marriage, motherhood, and sacrifice. Each story stages an existence compressed within rigid social roles, where individual feelings conflict with community expectations. The stories seek no solutions but record destinies.',
                    'analisi': 'Capuana adopts a verismo gaze that neither judges nor consoles. Language is modeled on speech, narrative structure is essential. Le paesane constitutes a precious document on the female condition in the Sicilian rural world and on the interaction between individual and tradition.'
                }
            }
        },
        {
            'titolo': 'C’era una volta…',
            'slug': 'cera-una-volta',
            'anno_pubblicazione': 1882,
            'breve_descrizione': 'Raccolta di fiabe popolari riscritte da Capuana, tra realismo, oralità e immaginazione fantastica.',
            'trama': 'Le fiabe riprendono motivi della tradizione popolare siciliana: re, fate, contadini, orchi, animali parlanti e prove iniziatiche. Pur nella struttura fiabesca, i racconti mantengono una concretezza sorprendente: la fame, la fatica e l’astuzia contadina convivono con l’elemento magico. Il meraviglioso non cancella mai del tutto la durezza della realtà.',
            'analisi': 'Capuana dimostra che il Verismo non è incompatibile con il fantastico. Anzi, il mondo fiabesco diventa un altro strumento per raccontare la mentalità popolare. Questa raccolta è fondamentale per comprendere l’interesse di Capuana per l’antropologia, il folklore e la psicologia collettiva.',
            'link_wikisource': 'https://it.wikisource.org/wiki/C%27era_una_volta..._Fiabe',
            'copertina_path': 'cera_una_volta.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'C\'era una volta…',
                    'breve_descrizione': 'Collection of folk tales rewritten by Capuana, blending realism, orality, and fantastic imagination.',
                    'trama': 'The tales draw on motifs from Sicilian folk tradition: kings, fairies, peasants, ogres, talking animals, and initiatory trials. Despite the fairy-tale structure, the stories maintain surprising concreteness: hunger, fatigue, and peasant cunning coexist with the magical element. The marvelous never completely erases the harshness of reality.',
                    'analisi': 'Capuana demonstrates that Verismo is not incompatible with the fantastic. Rather, the fairy-tale world becomes another tool for narrating popular mentality. This collection is fundamental to understanding Capuana\'s interest in anthropology, folklore, and collective psychology.'
                }
            }
        },
        {
            'titolo': 'Novelle del mondo occulto',
            'slug': 'novelle-del-mondo-occulto',
            'anno_pubblicazione': 1896,
            'breve_descrizione': 'Raccolta di racconti incentrati su spiritismo, mistero e fenomeni paranormali.',
            'trama': 'Le novelle presentano personaggi borghesi e intellettuali che entrano in contatto con eventi inspiegabili: sedute spiritiche, apparizioni, percezioni extrasensoriali. I protagonisti oscillano tra fede e scetticismo, tra razionalità scientifica e attrazione per l’ignoto, senza che il racconto offra mai una spiegazione definitiva.',
            'analisi': 'Capuana affronta il tema dell’occulto con rigore quasi sperimentale. Il soprannaturale non è mai puro effetto spettacolare, ma un campo di indagine sui limiti della conoscenza umana. Questa raccolta mostra il volto più moderno e inquieto dell’autore, in dialogo con la cultura europea di fine Ottocento.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_del_mondo_occulto',
            'copertina_path': 'novelle_del_mondo_occulto.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Novelle del mondo occulto',
                    'breve_descrizione': 'Collection of stories focused on spiritualism, mystery, and paranormal phenomena.',
                    'trama': 'The novellas present bourgeois and intellectual characters who come into contact with inexplicable events: spiritualist séances, apparitions, extrasensory perceptions. The protagonists oscillate between faith and skepticism, between scientific rationality and attraction to the unknown, without the narrative ever offering a definitive explanation.',
                    'analisi': 'Capuana approaches the theme of the occult with almost experimental rigor. The supernatural is never pure spectacular effect but a field of investigation into the limits of human knowledge. This collection shows the most modern and restless face of the author, in dialogue with late-nineteenth-century European culture.'
                }
            }
        },
        {
            'titolo': 'Il drago',
            'slug': 'il-drago',
            'anno_pubblicazione': 1898,
            'breve_descrizione': 'Romanzo fantastico che fonde fiaba, allegoria e osservazione sociale.',
            'trama': 'Attraverso una vicenda simbolica, Capuana racconta un mondo governato da forze oscure e irrazionali, in cui il “drago” assume molteplici significati: paura, potere, pulsione distruttiva. I personaggi si muovono in un universo sospeso tra sogno e realtà, dove il confine tra bene e male resta ambiguo.',
            'analisi': 'Il drago conferma l’originalità di Capuana rispetto al Verismo più ortodosso. Il fantastico diventa metafora della condizione umana e sociale. Il romanzo dialoga con il simbolismo europeo e anticipa alcune suggestioni del primo Novecento.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Il_drago',
            'copertina_path': 'il_drago.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Il drago',
                    'breve_descrizione': 'Fantastic novel that blends fairy tale, allegory, and social observation.',
                    'trama': 'Through a symbolic story, Capuana narrates a world governed by dark and irrational forces, in which the \"dragon\" assumes multiple meanings: fear, power, destructive impulse. The characters move in a universe suspended between dream and reality, where the boundary between good and evil remains ambiguous.',
                    'analisi': 'The Dragon confirms Capuana\'s originality compared to more orthodox Verismo. The fantastic becomes a metaphor for the human and social condition. The novel dialogues with European symbolism and anticipates some suggestions of the early twentieth century.'
                }
            }
        },
        {
            'titolo': 'Sogno di un tramonto d’autunno',
            'slug': 'sogno-di-un-tramonto-dautunno',
            'anno_pubblicazione': 1898,
            'breve_descrizione': 'Racconto di forte intensità introspettiva, sospeso tra realtà e visione.',
            'trama': 'Il protagonista vive un’esperienza onirica durante un tramonto autunnale che diventa occasione di riflessione sul tempo, sulla memoria e sulla fine delle illusioni. Il confine tra sogno e veglia è volutamente incerto, e l’atmosfera malinconica domina l’intero racconto.',
            'analisi': 'Questo testo mostra la componente lirica e simbolica di Capuana. Pur restando ancorato all’osservazione psicologica, l’autore sperimenta forme narrative che si allontanano dal Verismo classico e si avvicinano a una sensibilità decadente.',
            'link_wikisource': 'https://it.wikisource.org/wiki/Sogno_di_un_tramonto_d%27autunno',
            'copertina_path': 'sogno_di_un_tramonto_dautunno.jpg',
            'traduzioni': {
                'en': {
                    'titolo': 'Sogno di un tramonto d\'autunno',
                    'breve_descrizione': 'Story of strong introspective intensity, suspended between reality and vision.',
                    'trama': 'The protagonist experiences a dreamlike occurrence during an autumn sunset that becomes an occasion for reflection on time, memory, and the end of illusions. The boundary between dream and waking is deliberately uncertain, and a melancholic atmosphere dominates the entire story.',
                    'analisi': 'This text shows the lyrical and symbolic component of Capuana. While remaining anchored to psychological observation, the author experiments with narrative forms that move away from classical Verismo and approach a decadent sensibility.'
                }
            }
        }
    ]
    
    for opera_data in opere_capuana:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': capuana,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = capuana
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        
        # Copia la copertina se specificata e non esiste già
        if 'copertina_path' in opera_data and not opera.copertina:
            # Salva in media/copertine/opere_Capuana/
            copertina_path = copy_static_to_media(opera_data['copertina_path'], f"copertine/opere_Capuana/{opera_data['slug']}.jpg")
            if copertina_path:
                media_path = os.path.join(settings.MEDIA_ROOT, copertina_path)
                with open(media_path, 'rb') as f:
                    opera.copertina.save(f"{opera_data['slug']}.jpg", File(f), save=False)
        
        # Se non c'è copertina (o perché non specificata o perché il file non esiste), usa il placeholder
        if not opera.copertina:
            opera.copertina.name = 'copertine/opere_Capuana/placeHolder_capuana.jpeg'
        
        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.breve_descrizione = opera_data.get('breve_descrizione', '')
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        
        # Salva traduzioni inglesi se disponibili
        if 'traduzioni' in opera_data and 'en' in opera_data['traduzioni']:
            opera.set_current_language('en')
            opera.titolo = opera_data['traduzioni']['en']['titolo']
            opera.breve_descrizione = opera_data['traduzioni']['en'].get('breve_descrizione', '')
            opera.trama = opera_data['traduzioni']['en'].get('trama', '')
            opera.analisi = opera_data['traduzioni']['en'].get('analisi', '')
            opera.save()
        
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # EVENTI CON FOTO
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA EVENTI CON FOTO")
    print("="*70)
    
    eventi_data = [
        {
            'titolo': 'Presentazione del romanzo "I Malavoglia"',
            'slug': 'presentazione-i-malavoglia',
            'descrizione': '''Il Parco Letterario Giovanni Verga e Luigi Capuana organizza una serata speciale dedicata al capolavoro
di Giovanni Verga. L'evento prevede una lettura guidata dei passi più significativi del romanzo,
seguita da un dibattito con esperti letterari e studiosi del verismo siciliano.

Saranno presenti:
- Letture a cura di attori professionisti
- Analisi critica dell'opera
- Dibattito con il pubblico
- Degustazione di prodotti tipici siciliani

L'evento si terrà nella suggestiva cornice di Aci Trezza, luogo natale del romanzo.''',
            'data_inizio': datetime(2025, 12, 15, 18, 30),
            'data_fine': datetime(2025, 12, 15, 22, 00),
            'luogo': 'Aci Trezza - Teatro Comunale',
            'indirizzo': 'Via Teatro, 1 - 95021 Aci Trezza (CT)',
            'immagine_path': 'vizzini/casaVerga.jpg',
            'is_active': True
        },
        {
            'titolo': 'Visita guidata ai luoghi verghiani',
            'slug': 'visita-guidata-luoghi-verghiani',
            'descrizione': '''Scopri i luoghi che hanno ispirato le opere di Giovanni Verga in una visita guidata
esclusiva organizzata dal Parco Letterario Giovanni Verga e Luigi Capuana.

Il percorso toccherà:
- La casa di Giovanni Verga a Vizzini
- I luoghi di "I Malavoglia" ad Aci Trezza
- I paesaggi che hanno ispirato "Vita dei campi"
- Le chiese e i monumenti storici menzionati nelle opere

La visita è gratuita e dura circa 3 ore. Prenotazione obbligatoria.''',
            'data_inizio': datetime(2025, 11, 20, 9, 00),
            'data_fine': datetime(2025, 11, 20, 12, 00),
            'luogo': 'Vizzini - Casa di Giovanni Verga',
            'indirizzo': 'Via Giovanni Verga - 95049 Vizzini (CT)',
            'immagine_path': 'vizzini/centrostorico.jpg',
            'is_active': True
        },
        {
            'titolo': 'Visita guidata alla casa di Luigi Capuana',
            'slug': 'visita-casa-capuana',
            'descrizione': '''Visita esclusiva alla casa natale di Luigi Capuana a Mineo, uno dei luoghi più 
significativi del Parco Letterario Giovanni Verga e Luigi Capuana.

Durante la visita potrete:
- Visitare le stanze dove visse Capuana
- Ammirare i manoscritti e i documenti originali
- Scoprire la biblioteca personale dello scrittore
- Conoscere la storia e le tradizioni di Mineo

La visita è guidata da esperti del Parco Letterario.''',
            'data_inizio': datetime(2025, 11, 25, 10, 00),
            'data_fine': datetime(2025, 11, 25, 12, 30),
            'luogo': 'Mineo - Casa Museo Luigi Capuana',
            'indirizzo': 'Via Luigi Capuana - 95044 Mineo (CT)',
            'immagine_path': 'mineo/Casa-Luigi-Capuana.jpg',
            'is_active': True
        },
        {
            'titolo': 'Festival del Verismo Siciliano',
            'slug': 'festival-verismo-siciliano',
            'descrizione': '''Il Festival del Verismo Siciliano è un evento annuale che celebra la letteratura 
verista e la cultura siciliana attraverso spettacoli, conferenze e laboratori.

Il festival prevede:
- Spettacoli teatrali tratti dalle opere di Verga e Capuana
- Conferenze con critici letterari e studiosi
- Laboratori di scrittura creativa
- Mostre fotografiche sui luoghi verghiani
- Degustazioni di prodotti tipici siciliani

L'evento si svolge nei comuni del Parco Letterario Giovanni Verga e Luigi Capuana.''',
            'data_inizio': datetime(2026, 3, 15, 10, 00),
            'data_fine': datetime(2026, 3, 17, 22, 00),
            'luogo': 'Vizzini, Mineo e Licodia Eubea',
            'indirizzo': 'Vari comuni del Parco Letterario',
            'immagine_path': 'vizzini/festa.jpeg',
            'is_active': True
        },
        {
            'titolo': 'Convegno: Il Verismo oggi',
            'slug': 'convegno-verismo-oggi',
            'descrizione': '''Un convegno internazionale dedicato all'attualità del verismo nella letteratura
contemporanea. Interverranno critici letterari, scrittori e accademici da tutta Italia.

Temi trattati:
- L'eredità del verismo nella narrativa italiana contemporanea
- Verga e Capuana: maestri del realismo
- Il verismo siciliano e la letteratura europea
- Nuove prospettive critiche sul movimento verista

L'evento è accreditato per la formazione docenti.''',
            'data_inizio': datetime(2026, 1, 25, 9, 30),
            'data_fine': datetime(2026, 1, 25, 18, 00),
            'luogo': 'Università di Catania - Aula Magna',
            'indirizzo': 'Via Biblioteca, 4 - 95124 Catania',
            'immagine_path': 'vizzini/duomo.jpg',
            'is_active': True
        },
    ]
    
    for evento_data in eventi_data:
        evento, created = Evento.objects.get_or_create(
            slug=evento_data['slug'],
            defaults={
                'data_inizio': evento_data['data_inizio'],
                'data_fine': evento_data.get('data_fine'),
                'is_active': evento_data.get('is_active', True)
            }
        )
        if not created:
            evento.data_inizio = evento_data['data_inizio']
            evento.data_fine = evento_data.get('data_fine')
            evento.is_active = evento_data.get('is_active', True)
        
        # Copia l'immagine se specificata
        if 'immagine_path' in evento_data and not evento.immagine:
            image_path = copy_static_to_media(evento_data['immagine_path'], f"eventi/{evento_data['slug']}.jpg")
            if image_path:
                media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(media_path, 'rb') as f:
                    evento.immagine.save(f"{evento_data['slug']}.jpg", File(f), save=False)
        
        evento.set_current_language('it')
        evento.titolo = evento_data['titolo']
        evento.descrizione = evento_data['descrizione']
        evento.luogo = evento_data['luogo']
        evento.indirizzo = evento_data.get('indirizzo', '')
        evento.save()
        if created:
            print(f"✓ Creato evento: {evento.titolo} ({evento.data_inizio.date()})")
        else:
            print(f"• Evento aggiornato: {evento.titolo}")
    
    # ========================================================================
    # NOTIZIE CON FOTO
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA NOTIZIE CON FOTO")
    print("="*70)
    
    notizie_data = [
        {
            'titolo': 'Nuova pubblicazione: Guida ai luoghi verghiani',
            'slug': 'guida-luoghi-verghiani',
            'contenuto': '''È disponibile la nuova guida "Alla scoperta dei luoghi verghiani", una pubblicazione
bilingue (italiano-inglese) che accompagna i visitatori alla scoperta dei luoghi che hanno ispirato
le opere di Giovanni Verga.

La guida, realizzata in collaborazione con l'Università di Catania, contiene:
- Mappe dettagliate dei percorsi letterari
- Descrizioni storiche e letterarie dei luoghi
- Fotografie d'epoca e moderne
- Citazioni dalle opere di Verga
- Informazioni pratiche per i visitatori

La pubblicazione è disponibile gratuitamente presso gli uffici del Parco e sul nostro sito web.''',
            'riassunto': 'Disponibile la nuova guida bilingue per scoprire i luoghi che hanno ispirato le opere di Giovanni Verga.',
            'immagine_path': 'vizzini/borgo.jpg',
            'is_active': True
        },
        {
            'titolo': 'Progetto educativo: Il verismo a scuola',
            'slug': 'progetto-educativo-verismo',
            'contenuto': '''Il Parco Letterario Giovanni Verga e Luigi Capuana ha avviato un nuovo progetto educativo rivolto
agli studenti delle scuole superiori siciliane.

Il progetto "Il verismo a scuola" prevede:
- Visite guidate gratuite per le classi
- Laboratori di scrittura creativa ispirati al verismo
- Incontri con scrittori e critici letterari
- Concorso letterario per studenti
- Materiali didattici digitali

L'iniziativa coinvolgerà oltre 50 istituti scolastici e mira a far conoscere il movimento
verista alle nuove generazioni, stimolando l'interesse per la letteratura e la cultura siciliana.

Le scuole interessate possono contattare gli uffici del Parco per informazioni e prenotazioni.''',
            'riassunto': 'Nuovo progetto educativo per portare il verismo nelle scuole siciliane con visite guidate e laboratori.',
            'immagine_path': 'mineo/premio-luigi.jpg',
            'is_active': True
        },
        {
            'titolo': 'Restauro della casa di Giovanni Verga a Vizzini',
            'slug': 'restauro-casa-verga',
            'contenuto': '''È stato completato il restauro della casa natale di Giovanni Verga a Vizzini. 
Il restauro ha interessato sia la struttura esterna che gli interni, riportando l'edificio 
all'antico splendore.

La casa, ora museo, sarà aperta al pubblico a partire dal prossimo mese e ospiterà:
- Mostre permanenti sulla vita e le opere di Verga
- Biblioteca specializzata sul verismo
- Archivio documenti e manoscritti
- Spazi per eventi e conferenze

Il restauro è stato possibile grazie al contributo della Regione Siciliana e dell'Unione Europea.''',
            'riassunto': 'Completato il restauro della casa natale di Giovanni Verga a Vizzini, che diventerà un museo aperto al pubblico.',
            'immagine_path': 'vizzini/casaVerga.jpg',
            'is_active': True
        },
        {
            'titolo': 'Settimana Santa a Licodia Eubea: tradizioni e letteratura',
            'slug': 'settimana-santa-licodia',
            'contenuto': '''Il Parco Letterario Giovanni Verga e Luigi Capuana partecipa alle celebrazioni della Settimana Santa a Licodia Eubea,
un evento che unisce tradizione religiosa e cultura letteraria.

Durante la Settimana Santa si terranno:
- Processioni storiche per le vie del paese
- Letture pubbliche di brani tratti dalle opere veriste
- Visite guidate ai luoghi storici
- Mostre fotografiche sulle tradizioni locali

L'evento rappresenta un'occasione unica per scoprire come le tradizioni siciliane siano state 
raccontate dai grandi autori del verismo.''',
            'riassunto': 'Il Parco Letterario partecipa alle celebrazioni della Settimana Santa a Licodia Eubea, unendo tradizione e letteratura.',
            'immagine_path': 'licodia/settimana_santa.jpg',
            'is_active': True
        },
    ]
    
    for notizia_data in notizie_data:
        notizia, created = Notizia.objects.get_or_create(
            slug=notizia_data['slug'],
            defaults={
                'is_active': notizia_data.get('is_active', True)
            }
        )
        if not created:
            notizia.is_active = notizia_data.get('is_active', True)
        
        # Copia l'immagine se specificata
        if 'immagine_path' in notizia_data and not notizia.immagine:
            image_path = copy_static_to_media(notizia_data['immagine_path'], f"notizie/{notizia_data['slug']}.jpg")
            if image_path:
                media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(media_path, 'rb') as f:
                    notizia.immagine.save(f"{notizia_data['slug']}.jpg", File(f), save=False)
        
        notizia.set_current_language('it')
        notizia.titolo = notizia_data['titolo']
        notizia.contenuto = notizia_data['contenuto']
        notizia.riassunto = notizia_data['riassunto']
        notizia.save()
        if created:
            print(f"✓ Creata notizia: {notizia.titolo}")
        else:
            print(f"• Notizia aggiornata: {notizia.titolo}")
    
    # ========================================================================
    # ARCHIVIO FOTOGRAFICO
    # ========================================================================
    print("\n" + "="*70)
    print("POPOLAMENTO ARCHIVIO FOTOGRAFICO")
    print("="*70)
    
    # Pulisce le foto esistenti per evitare duplicati o dati sporchi
    FotoArchivio.objects.all().delete()
    print("• Archivio fotografico resettato")

    # Configurazione cartelle sorgente (percorso assoluto)
    base_media_path = os.path.join(settings.MEDIA_ROOT, 'archivio_fotografico')
    path_verga = os.path.join(base_media_path, 'foto_Verga')
    path_capuana = os.path.join(base_media_path, 'foto_Capuana')

    # Pulizia file fisici nella cartella archivio_fotografico (escludendo le sottocartelle sorgente)
    if os.path.exists(base_media_path):
        print("• Pulizia file fisici duplicati...")
        for filename in os.listdir(base_media_path):
            file_path = os.path.join(base_media_path, filename)
            # Se è un file e non è una directory (quindi preserva foto_Verga e foto_Capuana)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"  ⚠️ Impossibile eliminare {filename}: {e}")

    def add_photos_from_dir(directory, autore_code):
        if not os.path.exists(directory):
            print(f"⚠ Directory non trovata: {directory}")
            return
        
        files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        ordine = 0
        
        for filename in files:
            source_path = os.path.join(directory, filename)
            
            # Crea l'oggetto FotoArchivio
            foto = FotoArchivio()
            
            # Apri il file e salvalo nel campo immagine
            with open(source_path, 'rb') as f:
                # Il nome del file nel database sarà lo stesso dell'originale
                foto.immagine.save(filename, File(f), save=False)
            
            foto.ordine = ordine
            foto.autore = autore_code
            foto.is_active = True
            
            # Imposta titolo e descrizione (usando il nome del file come base)
            titolo_base = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
            
            foto.set_current_language('it')
            foto.titolo = titolo_base
            foto.descrizione = f"Foto d'archivio di {autore_code.capitalize()}: {titolo_base}"
            foto.categoria = 'Archivio Storico'
            foto.save()
            
            print(f"✓ Aggiunta foto {autore_code}: {filename}")
            ordine += 1

    # Popola dalle due cartelle specifiche
    print("\n--- Caricamento foto Verga ---")
    add_photos_from_dir(path_verga, 'VERGA')
    
    print("\n--- Caricamento foto Capuana ---")
    add_photos_from_dir(path_capuana, 'CAPUANA')
    
    print(f"DEBUG: Foto Verga nel DB: {FotoArchivio.objects.filter(autore='VERGA').count()}")
    print(f"DEBUG: Foto Capuana nel DB: {FotoArchivio.objects.filter(autore='CAPUANA').count()}")

    # ========================================================================
    # ITINERARI VERGHIANI E CAPUANIANI
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA ITINERARI")
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
    
    # ========================================================================
    # AGGIORNAMENTO COORDINATE ITINERARI PER MAPPA
    # ========================================================================
    update_itinerari_coordinates()
    
    # ========================================================================
    # RIEPILOGO FINALE
    # ========================================================================
    print("\n" + "="*70)
    print("POPOLAMENTO COMPLETATO CON SUCCESSO!")
    print("="*70)
    print(f"\nTotale autori: {Autore.objects.count()}")
    print(f"Totale opere: {Opera.objects.count()}")
    print(f"  - Opere di Verga: {Opera.objects.filter(autore=verga).count()}")
    print(f"  - Opere di Capuana: {Opera.objects.filter(autore=capuana).count()}")
    print(f"Totale eventi: {Evento.objects.count()}")
    print(f"Totale notizie: {Notizia.objects.count()}")
    print(f"Totale foto archivio: {FotoArchivio.objects.count()}")
    print(f"Totale itinerari: {Itinerario.objects.count()}")
    print(f"  - Itinerari verghiani: {Itinerario.objects.filter(tipo='verghiano').count()}")
    print(f"  - Itinerari capuaniani: {Itinerario.objects.filter(tipo='capuaniano').count()}")
    print(f"  - Itinerari tematici: {Itinerario.objects.filter(tipo='tematico').count()}")
    print(f"\nPuoi ora avviare il server con:")
    print("  python manage.py runserver")
    print("\nE visitare:")
    print("  - Biblioteca: http://127.0.0.1:8000/biblioteca/")
    print("  - Eventi: http://127.0.0.1:8000/eventi/")
    print("  - Notizie: http://127.0.0.1:8000/notizie/")
    print("  - Archivio Fotografico: http://127.0.0.1:8000/archivio/")
    print("  - Itinerari: http://127.0.0.1:8000/itinerari-verghiani/")


def update_itinerari_coordinates():
    """Aggiorna le coordinate GPS degli itinerari per la mappa interattiva"""
    print("\n" + "="*70)
    print("AGGIORNAMENTO COORDINATE ITINERARI")
    print("="*70)
    
    # Itinerario "Sulle tracce de I Malavoglia"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-malavoglia')
        itinerario.coordinate_tappe = [
            {
                "nome": "Aci Trezza - Casa del Nespolo",
                "coords": [37.5614, 15.1595],
                "descrizione": "La casa della famiglia Malavoglia, protagonista del romanzo",
                "order": 1
            },
            {
                "nome": "Faraglioni dei Ciclopi",
                "coords": [37.5589, 15.1642],
                "descrizione": "Gli iconici scogli di basalto, teatro delle vicende marinare",
                "order": 2
            },
            {
                "nome": "Chiesa di San Giovanni Battista",
                "coords": [37.5625, 15.1580],
                "descrizione": "La chiesa del paese dove la famiglia partecipava alle funzioni",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#1976D2'
        itinerario.icona_percorso = '🌊'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-malavoglia' non trovato")
    
    # Itinerario "Il mondo di Mastro-don Gesualdo"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-mastro-don-gesualdo')
        itinerario.coordinate_tappe = [
            {
                "nome": "Vizzini - Piazza Umberto I",
                "coords": [37.1584, 14.7443],
                "descrizione": "Il cuore del paese, scenario del romanzo",
                "order": 1
            },
            {
                "nome": "Palazzo Verga",
                "coords": [37.1578, 14.7438],
                "descrizione": "Dimora storica che ispirò lo scrittore",
                "order": 2
            },
            {
                "nome": "Chiesa di San Giovanni Battista",
                "coords": [37.1590, 14.7450],
                "descrizione": "Chiesa barocca frequentata dalla nobiltà locale",
                "order": 3
            },
            {
                "nome": "La Cunziria",
                "coords": [37.1570, 14.7445],
                "descrizione": "L'antica conceria, simbolo della Vizzini dell'800",
                "order": 4
            }
        ]
        itinerario.colore_percorso = '#8B4513'
        itinerario.icona_percorso = '🏛️'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-mastro-don-gesualdo' non trovato")
    
    # Itinerario "I luoghi di Vita dei campi"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-vita-dei-campi')
        itinerario.coordinate_tappe = [
            {
                "nome": "Campagne di Vizzini",
                "coords": [37.1700, 14.7500],
                "descrizione": "Paesaggi rurali immutati nel tempo",
                "order": 1
            },
            {
                "nome": "Antica Masseria",
                "coords": [37.1650, 14.7600],
                "descrizione": "Esempio di architettura rurale siciliana",
                "order": 2
            },
            {
                "nome": "Bosco di Santo Pietro",
                "coords": [37.1550, 14.7700],
                "descrizione": "Area boschiva che fa da sfondo alle novelle",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#388E3C'
        itinerario.icona_percorso = '🌾'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-vita-dei-campi' non trovato")
    
    # Itinerario "La Cunziria e il centro storico di Vizzini"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-cunziria')
        itinerario.coordinate_tappe = [
            {
                "nome": "La Cunziria",
                "coords": [37.1570, 14.7445],
                "descrizione": "L'antica conceria di Vizzini",
                "order": 1
            },
            {
                "nome": "Casa Museo Giovanni Verga",
                "coords": [37.1578, 14.7438],
                "descrizione": "La casa dello scrittore",
                "order": 2
            },
            {
                "nome": "Duomo di Vizzini",
                "coords": [37.1590, 14.7450],
                "descrizione": "La cattedrale del paese",
                "order": 3
            },
            {
                "nome": "Piazza Umberto I",
                "coords": [37.1584, 14.7443],
                "descrizione": "La piazza principale",
                "order": 4
            }
        ]
        itinerario.colore_percorso = '#D32F2F'
        itinerario.icona_percorso = '🏺'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-cunziria' non trovato")
    
    # Itinerario Mineo - Capuana
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-capuana-mineo')
        itinerario.coordinate_tappe = [
            {
                "nome": "Casa Natale Luigi Capuana",
                "coords": [37.2667, 14.6833],
                "descrizione": "Museo dedicato allo scrittore",
                "order": 1
            },
            {
                "nome": "Centro Storico di Mineo",
                "coords": [37.2670, 14.6840],
                "descrizione": "Il cuore della città di Capuana",
                "order": 2
            },
            {
                "nome": "Chiesa Madre",
                "coords": [37.2665, 14.6835],
                "descrizione": "Importante chiesa del paese",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#7B1FA2'
        itinerario.icona_percorso = '📖'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-capuana-mineo' non trovato")
    
    print("\n" + "="*70)
    print("AGGIORNAMENTO COORDINATE COMPLETATO!")
    print("="*70)


def check_database():
    """Verifica lo stato del database e mostra statistiche"""
    print("\n" + "="*70)
    print("VERIFICA DATABASE")
    print("="*70)
    
    # Autori
    print("\n--- AUTORI ---")
    autori = Autore.objects.all()
    if autori.exists():
        for autore in autori:
            opere_count = Opera.objects.filter(autore=autore).count()
            print(f"  • {autore.nome} (slug: {autore.slug}) - {opere_count} opere")
    else:
        print("  Nessun autore trovato")
    
    # Opere
    print("\n--- OPERE ---")
    print(f"  Totale opere: {Opera.objects.count()}")
    opere_senza_link = Opera.objects.filter(link_wikisource='').count()
    if opere_senza_link > 0:
        print(f"  ⚠️  {opere_senza_link} opere senza link Wikisource")
    opere_senza_copertina = Opera.objects.filter(copertina='').count()
    if opere_senza_copertina > 0:
        print(f"  ℹ️  {opere_senza_copertina} opere senza copertina")
    
    # Eventi
    print("\n--- EVENTI ---")
    print(f"  Totale eventi: {Evento.objects.count()}")
    print(f"  Eventi attivi: {Evento.objects.filter(is_active=True).count()}")
    eventi_futuri = Evento.objects.filter(data_inizio__gte=datetime.now()).count()
    print(f"  Eventi futuri: {eventi_futuri}")
    
    # Notizie
    print("\n--- NOTIZIE ---")
    print(f"  Totale notizie: {Notizia.objects.count()}")
    print(f"  Notizie attive: {Notizia.objects.filter(is_active=True).count()}")
    
    # Archivio Fotografico
    print("\n--- ARCHIVIO FOTOGRAFICO ---")
    print(f"  Totale foto: {FotoArchivio.objects.count()}")
    print(f"  Foto attive: {FotoArchivio.objects.filter(is_active=True).count()}")
    
    # Itinerari
    print("\n--- ITINERARI ---")
    print(f"  Totale itinerari: {Itinerario.objects.count()}")
    print(f"  Itinerari attivi: {Itinerario.objects.filter(is_active=True).count()}")
    print(f"  Itinerari verghiani: {Itinerario.objects.filter(tipo='verghiano').count()}")
    print(f"  Itinerari capuaniani: {Itinerario.objects.filter(tipo='capuaniano').count()}")
    itinerari_senza_coords = Itinerario.objects.filter(coordinate_tappe__isnull=True).count()
    if itinerari_senza_coords > 0:
        print(f"  ⚠️  {itinerari_senza_coords} itinerari senza coordinate GPS")
        print(f"     Esegui: python populate_db_complete.py --update-coords")
    
    print("\n" + "="*70)
    print("VERIFICA COMPLETATA")
    print("="*70)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--create-superuser':
            create_superuser()
        elif sys.argv[1] == '--update-coords':
            update_itinerari_coordinates()
        elif sys.argv[1] == '--check':
            check_database()
        elif sys.argv[1] == '--help':
            print(__doc__)
        else:
            print(f"Opzione sconosciuta: {sys.argv[1]}")
            print("Usa --help per vedere le opzioni disponibili")
    else:
        populate()
