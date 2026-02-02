# Django imports
from django.urls import path

# Local imports
from .views import (
    home_view,
    opere_per_autore_view, opera_detail_view,
    personaggi_lessico_view, luoghi_opere_view,
    eventi_view, evento_detail_view,
    notizie_view, notizia_detail_view,
    documenti_view, documento_detail_view, verga_capuana_fotografi_view,
    itinerari_verghiani_view, itinerari_capuaniani_view, 
    itinerari_tematici_view, itinerario_detail_view,
    licodia_view, mineo_view, vizzini_view,
    missione_visione_view, comitato_tecnico_scientifico_view,
    comitato_regolamento_view, regolamenti_documenti_view,
    partner_rete_territoriale_view, accrediti_finanziamenti_view,
    contatti_view,
    privacy_policy_view, note_legali_view, cookie_policy_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    
    # Pagine di presentazione per autore
    path('opere/<slug:autore_slug>/', opere_per_autore_view, name='opere_per_autore'),

    # Pagina di dettaglio/presentazione della singola opera
    path('opera/<slug:slug>/', opera_detail_view, name='opera_detail'),

    # Personaggi e Luoghi
    path('personaggi-lessico/', personaggi_lessico_view, name='personaggi_lessico'),
    path('luoghi-opere/', luoghi_opere_view, name='luoghi_opere'),

    # Eventi
    path('eventi/', eventi_view, name='eventi'),
    path('evento/<slug:slug>/', evento_detail_view, name='evento_detail'),

    # Notizie
    path('notizie/', notizie_view, name='notizie'),
    path('notizia/<slug:slug>/', notizia_detail_view, name='notizia_detail'),

    # Documenti e Studi
    path('documenti/', documenti_view, name='documenti'),
    path('documento/<slug:slug>/', documento_detail_view, name='documento_detail'),

    # Verga e Capuana Fotografi
    path('verga-capuana-fotografi/', verga_capuana_fotografi_view, name='verga_capuana_fotografi'),

    # Pagine statiche per i comuni del Parco
    path('licodia/', licodia_view, name='licodia'),
    path('mineo/', mineo_view, name='mineo'),
    path('vizzini/', vizzini_view, name='vizzini'),

    # Missione e Visione
    path('missione-visione/', missione_visione_view, name='missione_visione'),

    # Comitato Tecnico-Scientifico
    path('comitato/', comitato_tecnico_scientifico_view, name='comitato_tecnico_scientifico'),
    path('comitato/regolamento/', comitato_regolamento_view, name='comitato_regolamento'),

    # Regolamenti e Documenti
    path('regolamenti-documenti/', regolamenti_documenti_view, name='regolamenti_documenti'),

    # Partner e Rete Territoriale
    path('partner/', partner_rete_territoriale_view, name='partner_rete_territoriale'),

    # Accrediti e Finanziamenti
    # path('finanziamenti/', accrediti_finanziamenti_view, name='accrediti_finanziamenti'),
    
    # Contatti
    path('contatti/', contatti_view, name='contatti'),

    # Itinerari (liste e dettaglio)
    path('itinerari/verghiani/', itinerari_verghiani_view, name='itinerari_verghiani'),
    path('itinerari/capuaniani/', itinerari_capuaniani_view, name='itinerari_capuaniani'),
    path('cammino-del-verismo/', itinerari_tematici_view, name='cammino_del_verismo'),
    path('itinerario/<slug:slug>/', itinerario_detail_view, name='itinerario_detail'),
    
    # Pagine di conformità GDPR e PA
    path('privacy/', privacy_policy_view, name='privacy_policy'),
    path('note-legali/', note_legali_view, name='note_legali'),
    path('cookie-policy/', cookie_policy_view, name='cookie_policy'),
]
