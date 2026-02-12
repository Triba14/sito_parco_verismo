#!/usr/bin/env python3
"""
Script per popolare luoghi letterari e associazioni opere-luoghi-categorie
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Autore, Opera, LuogoLetterario, OperaInLuogo
from django.conf import settings

def populate_luoghi_e_opere():
    print("="*70)
    print("POPOLAMENTO LUOGHI E ASSOCIAZIONI OPERE")
    print("="*70)
    
    # Ottieni autori
    verga = Autore.objects.get(slug='giovanni-verga')
    capuana = Autore.objects.get(slug='luigi-capuana')
    
    # ========================================================================
    # OPERE DI VERGA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI GIOVANNI VERGA")
    print("="*70)
    
    opere_verga_data = {
        'Storia di una capinera': 'https://it.wikisource.org/wiki/Storia_di_una_capinera',
        'Mastro-don Gesualdo': 'https://it.wikisource.org/wiki/Mastro-don_Gesualdo',
        'La Duchessa di Leyra': 'https://it.wikisource.org/wiki/La_Duchessa_di_Leyra',
        'Jeli il pastore': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Jeli_il_pastore',
        'Cavalleria rusticana': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Cavalleria_rusticana',
        'Guerra di santi': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/Guerra_di_santi',
        'Il Reverendo': 'https://it.wikisource.org/wiki/Novelle_rusticane/Il_Reverendo',
        'Don Licciu Papa': 'https://it.wikisource.org/wiki/Novelle_rusticane/Don_Licciu_papa',
        'La roba': 'https://it.wikisource.org/wiki/Novelle_rusticane/La_roba',
        'Pane nero': 'https://it.wikisource.org/wiki/Novelle_rusticane/Pane_nero',
        'Di là del mare': 'https://it.wikisource.org/wiki/Novelle_rusticane/Di_là_del_mare',
        "L'Opera del Divino Amore": "https://it.wikisource.org/wiki/Don_Candeloro_e_C.i/L%27opera_del_Divino_Amore",
        'La vocazione di suor Agnese': 'https://it.wikisource.org/wiki/Don_Candeloro_e_C.i/La_vocazione_di_suor_Agnese',
        'Cavalleria rusticana (teatro)': 'https://it.wikisource.org/wiki/Cavalleria_rusticana_(dramma)',
        'La lupa': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/La_lupa',
        'La chiave d\'oro': 'https://it.wikisource.org/wiki/Drammi_intimi/La_chiave_d%27oro',
        'La Lupa (teatro)': 'https://it.wikisource.org/wiki/La_Lupa_(dramma)',
        "L'amante di Gramigna": "https://it.wikisource.org/wiki/Vita_dei_campi_(1881)/L%27amante_di_Gramigna",
        'Vagabondaggio': 'https://it.wikisource.org/wiki/Vagabondaggio',
        'Papa Sisto': 'https://it.wikisource.org/wiki/Don_Candeloro_e_C.i/Papa_Sisto',
        'Il Carnevale fallo con chi vuoi; Pasqua e Natale falli con i tuoi': 'https://it.wikisource.org/wiki/Racconti_e_bozzetti/-_Il_Carnevale_fallo_con_chi_vuoi;_-_Pasqua_e_Natale_falli_con_i_tuoi_-',
    }
    
    opere_verga_objects = {}
    for titolo, link in opere_verga_data.items():
        slug = titolo.lower().replace(' ', '-').replace('\'', '').replace('(teatro)', '-teatro').replace(';', '').replace(',', '')
        
        opera, created = Opera.objects.get_or_create(
            slug=slug,
            defaults={
                'autore': verga,
                'link_fonte': link
            }
        )
        if not created:
            opera.autore = verga
            opera.link_fonte = link
        
        copertina_filename = f"{slug}.jpg"
        copertina_path = os.path.join(settings.MEDIA_ROOT, 'copertine', 'opere_Verga', copertina_filename)
        
        if os.path.exists(copertina_path):
            opera.copertina.name = f'copertine/opere_Verga/{copertina_filename}'
        else:
            # Per le versioni teatro, prova a usare la copertina della versione base
            if '--teatro' in slug:
                base_slug = slug.replace('--teatro', '')
                base_copertina_filename = f"{base_slug}.jpg"
                base_copertina_path = os.path.join(settings.MEDIA_ROOT, 'copertine', 'opere_Verga', base_copertina_filename)
                
                if os.path.exists(base_copertina_path):
                    opera.copertina.name = f'copertine/opere_Verga/{base_copertina_filename}'
                else:
                    opera.copertina.name = 'copertine/opere_Verga/placeHolder_verga.jpeg'
            else:
                opera.copertina.name = 'copertine/opere_Verga/placeHolder_verga.jpeg'
        
        opera.set_current_language('it')
        opera.titolo = titolo
        opera.save()
        
        opere_verga_objects[titolo] = opera
        
        if created:
            print(f"✓ Creata opera: {opera.titolo}")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # OPERE DI CAPUANA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI LUIGI CAPUANA")
    print("="*70)
    
    opere_capuana_data = {
        "C'era una volta... Fiabe": {'link': 'https://it.wikisource.org/wiki/C%27era_una_volta..._Fiabe', 'fonte': 'wikisource'},
        'Malìa': {'link': 'https://it.wikisource.org/wiki/Malìa', 'fonte': 'wikisource'},
        'Il Marchese di Roccaverdina': {'link': 'https://it.wikisource.org/wiki/Il_Marchese_di_Roccaverdina', 'fonte': 'wikisource'},
        'Il Benefattore': {'link': 'https://archive.org/details/ilbenefattore00capugoog', 'fonte': 'internet_archive'},
        'Cardello': {'link': 'https://www.gutenberg.org/cache/epub/7267/pg7267-images.html', 'fonte': 'gutenberg'},
        'Nuove Paesane': {'link': 'https://archive.org/details/nuovepaesane00capuuoft', 'fonte': 'internet_archive'},
        'Fumando': {'link': 'https://archive.org/details/fumandonovelle00capugoog', 'fonte': 'internet_archive'},
        'Le paesane': {'link': 'https://archive.org/details/lepaesane00capugoog', 'fonte': 'internet_archive'},
        'Homo!': {'link': 'https://archive.org/details/homo00capugoog', 'fonte': 'internet_archive'},
    }
    
    opere_capuana_objects = {}
    for titolo, data in opere_capuana_data.items():
        slug = titolo.lower().replace(' ', '-').replace('\'', '').replace('!', '').replace('.', '').replace(',', '')
        
        opera, created = Opera.objects.get_or_create(
            slug=slug,
            defaults={
                'autore': capuana,
                'link_fonte': data['link'],
                'fonte_testo': data['fonte']
            }
        )
        if not created:
            opera.autore = capuana
            opera.link_fonte = data['link']
            opera.fonte_testo = data['fonte']
        
        copertina_filename = f"{slug}.jpg"
        copertina_path = os.path.join(settings.MEDIA_ROOT, 'copertine', 'opere_Capuana', copertina_filename)
        
        if os.path.exists(copertina_path):
            opera.copertina.name = f'copertine/opere_Capuana/{copertina_filename}'
        else:
            opera.copertina.name = 'copertine/opere_Capuana/placeHolder_capuana.jpeg'
        
        opera.set_current_language('it')
        opera.titolo = titolo
        opera.save()
        
        opere_capuana_objects[titolo] = opera
        
        if created:
            print(f"✓ Creata opera: {opera.titolo}")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # CREAZIONE LUOGHI LETTERARI
    # ========================================================================
    print("\n" + "="*70)
    print("CREAZIONE LUOGHI LETTERARI")
    print("="*70)
    
    vizzini, created = LuogoLetterario.objects.get_or_create(
        slug='vizzini',
        defaults={
            'nome': 'Vizzini',
            'ordine': 1
        }
    )
    if created:
        print(f"✓ Creato luogo: {vizzini.nome}")
    else:
        print(f"• Luogo già esistente: {vizzini.nome}")
    
    mineo, created = LuogoLetterario.objects.get_or_create(
        slug='mineo',
        defaults={
            'nome': 'Mineo',
            'ordine': 2
        }
    )
    if created:
        print(f"✓ Creato luogo: {mineo.nome}")
    else:
        print(f"• Luogo già esistente: {mineo.nome}")
    
    licodia, created = LuogoLetterario.objects.get_or_create(
        slug='licodia-eubea',
        defaults={
            'nome': 'Licodia Eubea',
            'ordine': 3
        }
    )
    if created:
        print(f"✓ Creato luogo: {licodia.nome}")
    else:
        print(f"• Luogo già esistente: {licodia.nome}")
    
    # ========================================================================
    # ASSOCIAZIONE OPERE - LUOGHI - CATEGORIE (VERGA)
    # ========================================================================
    print("\n" + "="*70)
    print("ASSOCIAZIONE OPERE DI VERGA A LUOGHI E CATEGORIE")
    print("="*70)
    
    # Vizzini - Verga
    vizzini_verga_romanzi = [
        'Storia di una capinera',
        'Mastro-don Gesualdo',
        'La Duchessa di Leyra'
    ]
    
    vizzini_verga_novelle = [
        'Jeli il pastore',
        'Cavalleria rusticana',
        'Guerra di santi',
        'Il Reverendo',
        'Don Licciu Papa',
        'La roba',
        'Pane nero',
        'Di là del mare',
        "L'Opera del Divino Amore",
        'La vocazione di suor Agnese'
    ]
    
    vizzini_verga_teatro = [
        'Cavalleria rusticana (teatro)'
    ]
    
    ordine = 1
    for titolo in vizzini_verga_romanzi:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=vizzini,
                categoria='romanzi',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Vizzini (Romanzi)")
            ordine += 1
    
    ordine = 1
    for titolo in vizzini_verga_novelle:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=vizzini,
                categoria='novelle',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Vizzini (Novelle)")
            ordine += 1
    
    ordine = 1
    for titolo in vizzini_verga_teatro:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=vizzini,
                categoria='teatro',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Vizzini (Teatro)")
            ordine += 1
    
    # Mineo - Verga
    mineo_verga_novelle = [
        'La lupa',
        'Pane nero',
        "La chiave d'oro"
    ]
    
    mineo_verga_teatro = [
        'La Lupa (teatro)'
    ]
    
    ordine = 1
    for titolo in mineo_verga_novelle:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=mineo,
                categoria='novelle',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Novelle)")
            ordine += 1
    
    ordine = 1
    for titolo in mineo_verga_teatro:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=mineo,
                categoria='teatro',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Teatro)")
            ordine += 1
    
    # Licodia Eubea - Verga
    licodia_verga_romanzi = [
        'Mastro-don Gesualdo'
    ]
    
    licodia_verga_novelle = [
        'Jeli il pastore',
        'Cavalleria rusticana',
        "L'amante di Gramigna",
        'Di là del mare',
        'Vagabondaggio',
        'Papa Sisto',
        'Il Carnevale fallo con chi vuoi; Pasqua e Natale falli con i tuoi'
    ]
    
    ordine = 1
    for titolo in licodia_verga_romanzi:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=licodia,
                categoria='romanzi',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Licodia Eubea (Romanzi)")
            ordine += 1
    
    ordine = 1
    for titolo in licodia_verga_novelle:
        if titolo in opere_verga_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_verga_objects[titolo],
                luogo=licodia,
                categoria='novelle',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Licodia Eubea (Novelle)")
            ordine += 1
    
    # ========================================================================
    # ASSOCIAZIONE OPERE - LUOGHI - CATEGORIE (CAPUANA)
    # ========================================================================
    print("\n" + "="*70)
    print("ASSOCIAZIONE OPERE DI CAPUANA A LUOGHI E CATEGORIE")
    print("="*70)
    
    # Mineo - Capuana
    mineo_capuana_fiabe = [
        "C'era una volta... Fiabe"
    ]
    
    mineo_capuana_teatro = [
        'Malìa'
    ]
    
    mineo_capuana_romanzi = [
        'Il Marchese di Roccaverdina',
        'Il Benefattore',
        'Cardello'
    ]
    
    mineo_capuana_novelle = [
        'Nuove Paesane',
        'Fumando',
        'Le paesane',
        'Homo!'
    ]
    
    ordine = 1
    for titolo in mineo_capuana_fiabe:
        if titolo in opere_capuana_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_capuana_objects[titolo],
                luogo=mineo,
                categoria='fiabe',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Fiabe)")
            ordine += 1
    
    ordine = 1
    for titolo in mineo_capuana_teatro:
        if titolo in opere_capuana_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_capuana_objects[titolo],
                luogo=mineo,
                categoria='teatro',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Teatro)")
            ordine += 1
    
    ordine = 1
    for titolo in mineo_capuana_romanzi:
        if titolo in opere_capuana_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_capuana_objects[titolo],
                luogo=mineo,
                categoria='romanzi',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Romanzi)")
            ordine += 1
    
    ordine = 1
    for titolo in mineo_capuana_novelle:
        if titolo in opere_capuana_objects:
            rel, created = OperaInLuogo.objects.get_or_create(
                opera=opere_capuana_objects[titolo],
                luogo=mineo,
                categoria='novelle',
                defaults={'ordine': ordine}
            )
            if created:
                print(f"  ✓ Associata: {titolo} → Mineo (Novelle)")
            ordine += 1
    
    print("\n" + "="*70)
    print("COMPLETATO!")
    print("="*70)

if __name__ == '__main__':
    populate_luoghi_e_opere()
