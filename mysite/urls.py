"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('parco_verismo/', include('parco_verismo.urls'))
"""

# Django imports
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

# Local imports

from parco_verismo.sitemaps import (
    StaticViewSitemap,
    OperaSitemap,
    AutoreSitemap,
    EventoSitemap,
    NotiziaSitemap,
    DocumentoSitemap,
    ItinerarioSitemap,
)

# Configurazione Sitemap per SEO
sitemaps = {
    "static": StaticViewSitemap,
    "opere": OperaSitemap,
    "autori": AutoreSitemap,
    "eventi": EventoSitemap,
    "notizie": NotiziaSitemap,
    "documenti": DocumentoSitemap,
    "itinerari": ItinerarioSitemap,
}

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

# URL con prefisso lingua (it/en)
urlpatterns += i18n_patterns(
    path("", include("parco_verismo.urls")),
    prefix_default_language=False,
)

# Admin senza prefisso lingua
urlpatterns += [
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
