from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    # Pagina principale della biblioteca con ricerca
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),
    
    # Pagine di presentazione per autore
    path('opere/<slug:autore_slug>/', views.opere_per_autore_view, name='opere_per_autore'),

    # Pagina di dettaglio/presentazione della singola opera
    path('opera/<slug:slug>/', views.opera_detail_view, name='opera_detail'),

    # Eventi e calendario
    path('eventi/', views.eventi_view, name='eventi'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('evento/<slug:slug>/', views.evento_detail_view, name='evento_detail'),

    # Notizie
    path('notizie/', views.notizie_view, name='notizie'),
    path('notizia/<slug:slug>/', views.notizia_detail_view, name='notizia_detail'),

    # Documenti e Studi
    path('documenti/', views.documenti_view, name='documenti'),
    path('documento/<slug:slug>/', views.documento_detail_view, name='documento_detail'),

    # Archivio Fotografico
    path('archivio/', views.archivio_fotografico_view, name='archivio_fotografico'),
]
