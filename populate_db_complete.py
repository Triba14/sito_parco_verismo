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
    Crea o aggiorna il superuser admin con password admin123
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
        # Aggiorna la password anche se esiste già
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"• Superuser aggiornato: {username} / {password}")

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
                    'titolo': 'Sparrow',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Daydreaming',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Rustic Chivalry',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The She-Wolf',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The House by the Medlar Tree',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The Property',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Liberty',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The Marquis of Roccaverdina',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The Country Women',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Once Upon a Time...',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Tales of the Occult World',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'The Dragon',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
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
                    'titolo': 'Dream of an Autumn Sunset',
                    'breve_descrizione': '',
                    'trama': '',
                    'analisi': ''
                }
            }
        },
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
    
    # Foto di Vizzini
    foto_vizzini = [
        # ('vizzini/casaVerga.jpg', 'Casa di Giovanni Verga', 'La casa natale di Giovanni Verga a Vizzini, oggi museo dedicato allo scrittore.', 'Luoghi'),
        # ('vizzini/centrostorico.jpg', 'Centro Storico di Vizzini', 'Il suggestivo centro storico di Vizzini con le sue caratteristiche vie.', 'Luoghi'),
        # ('vizzini/duomo.jpg', 'Duomo di Vizzini', 'Il Duomo di Vizzini, uno dei principali monumenti storici della città.', 'Luoghi'),
        # ('vizzini/borgo.jpg', 'Borgo di Vizzini', 'Il caratteristico borgo di Vizzini che ha ispirato molte opere di Verga.', 'Luoghi'),
        # ('vizzini/cunziria.jpg', 'La Cunziria', 'L\'antica conceria di Vizzini, luogo caratteristico del paese.', 'Luoghi'),
        # ('vizzini/festa.jpeg', 'Festa a Vizzini', 'Una festa tradizionale a Vizzini durante le celebrazioni estive.', 'Eventi'),
        # ('vizzini/festaRicotta.jpg', 'Festa della Ricotta', 'La tradizionale festa della ricotta di Vizzini.', 'Eventi'),
        # ('vizzini/processione.jpg', 'Processione religiosa', 'Una processione religiosa per le vie di Vizzini.', 'Eventi'),
        # ('vizzini/verga.jpeg', 'Giovanni Verga', 'Ritratto di Giovanni Verga, il grande scrittore verista.', 'Personaggi'),
        # ('vizzini/bosco.jpeg', 'Bosco di Vizzini', 'Il paesaggio naturale intorno a Vizzini.', 'Luoghi'),
    ]
    
    # Foto di Mineo
    foto_mineo = [
        # ('mineo/Casa-Luigi-Capuana.jpg', 'Casa di Luigi Capuana', 'La casa natale di Luigi Capuana a Mineo.', 'Luoghi'),
        # ('mineo/centro-storico.jpg', 'Centro Storico di Mineo', 'Il centro storico di Mineo con i suoi vicoli caratteristici.', 'Luoghi'),
        # ('mineo/castello.jpg', 'Castello di Mineo', 'L\'antico castello di Mineo, simbolo della città.', 'Luoghi'),
        # ('mineo/panorama.jpg', 'Panorama di Mineo', 'Il suggestivo panorama dai colli di Mineo.', 'Luoghi'),
        # ('mineo/chiesa.jpg', 'Chiesa di Mineo', 'Una delle chiese storiche di Mineo.', 'Luoghi'),
        # ('mineo/premio-luigi.jpg', 'Premio Luigi Capuana', 'La cerimonia del Premio letterario intitolato a Luigi Capuana.', 'Eventi'),
        # ('mineo/santa-agrippina.jpg', 'Chiesa di Santa Agrippina', 'La chiesa dedicata a Santa Agrippina, patrona di Mineo.', 'Luoghi'),
    ]
    
    # Foto di Licodia Eubea
    foto_licodia = [
        # ('licodia/hero-bg.jpg', 'Licodia Eubea', 'Veduta panoramica di Licodia Eubea.', 'Luoghi'),
        # ('licodia/chiesa_santa_margherita.jpg', 'Chiesa di Santa Margherita', 'La chiesa di Santa Margherita a Licodia Eubea.', 'Luoghi'),
        # ('licodia/colle_castello.jpg', 'Colle del Castello', 'Il colle del castello di Licodia Eubea.', 'Luoghi'),
        # ('licodia/panorama.jpg', 'Panorama di Licodia', 'Il suggestivo panorama dai colli di Licodia Eubea.', 'Luoghi'),
        # ('licodia/settimana_santa.jpg', 'Settimana Santa', 'Le celebrazioni della Settimana Santa a Licodia Eubea.', 'Eventi'),
        # ('licodia/festa_dell_uva.jpeg', 'Festa dell\'Uva', 'La tradizionale festa dell\'uva a Licodia Eubea.', 'Eventi'),
        # ('licodia/sagra.jpg', 'Sagra locale', 'Una sagra tradizionale a Licodia Eubea.', 'Eventi'),
    ]
    
    ordine = 0
    tutte_le_foto = [
        ('Vizzini', foto_vizzini),
        ('Mineo', foto_mineo),
        ('Licodia Eubea', foto_licodia),
    ]
    
    for comune, foto_list in tutte_le_foto:
        for immagine_path, titolo, descrizione, categoria in foto_list:
            # Controlla se la foto esiste già
            static_path = os.path.join(settings.BASE_DIR, 'parco_verismo', 'static', 'assets', 'img', immagine_path)
            if not os.path.exists(static_path):
                print(f"⚠ Immagine non trovata: {immagine_path}")
                continue
            
            # Crea il nome unico per la foto
            foto_slug = os.path.splitext(os.path.basename(immagine_path))[0]
            foto_id = f"{comune.lower()}_{foto_slug}"
            
            # Verifica se la foto esiste già nel database basandosi sul titolo
            foto = FotoArchivio.objects.filter(translations__titolo=titolo).first()
            if not foto:
                foto = FotoArchivio()
                created = True
            else:
                created = False
            
            if not foto.immagine:
                # Copia l'immagine
                image_path_rel = copy_static_to_media(immagine_path, f"archivio_fotografico/{comune.lower()}_{foto_slug}.jpg")
                if image_path_rel:
                    media_path = os.path.join(settings.MEDIA_ROOT, image_path_rel)
                    with open(media_path, 'rb') as f:
                        foto.immagine.save(f"{foto_slug}.jpg", File(f), save=False)
            
            foto.ordine = ordine
            foto.categoria = categoria
            foto.is_active = True
            foto.set_current_language('it')
            foto.titolo = titolo
            foto.descrizione = descrizione
            foto.save()
            
            if created:
                print(f"✓ Aggiunta foto: {foto.titolo} ({comune})")
            else:
                print(f"• Foto aggiornata: {foto.titolo}")
            
            ordine += 1
    
    # ========================================================================
    # ITINERARI VERGHIANI E CAPUANIANI
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA ITINERARI")
    print("="*70)
    
    itinerari_data = [
        # Esempio di itinerario (scommenta e modifica per aggiungere):
        # {
        #     'titolo': 'Titolo Itinerario',
        #     'slug': 'slug-itinerario',
        #     'descrizione': '''Descrizione dell'itinerario...''',
        #     'tipo': 'verghiano', # o 'capuaniano', 'tematico'
        #     'ordine': 1,
        #     'immagine_path': 'cartella/immagine.jpg',
        #     'durata_stimata': '2-3 ore',
        #     'difficolta': 'facile',
        #     'is_active': True
        # },
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
                'is_active': itinerario_data.get('is_active', True)
            }
        )
        
        if not created:
            itinerario.tipo = itinerario_data.get('tipo', 'verghiano')
            itinerario.ordine = itinerario_data.get('ordine', 1)
            itinerario.durata_stimata = itinerario_data.get('durata_stimata', '')
            itinerario.difficolta = itinerario_data.get('difficolta', 'facile')
            itinerario.link_maps = itinerario_data.get('link_maps', '')
            itinerario.is_active = itinerario_data.get('is_active', True)
        
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
    print("  - Calendario: http://127.0.0.1:8000/calendario/")
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

