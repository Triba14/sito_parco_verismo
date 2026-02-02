# Django imports
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Local imports
from .models import Opera, Evento, Notizia, Documento, Itinerario, Autore


class StaticViewSitemap(Sitemap):
    """Sitemap per le pagine statiche del sito"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'eventi',
            'notizie',
            'documenti',
            'verga_capuana_fotografi',
            'itinerari_verghiani',
            'itinerari_capuaniani',
            'cammino_del_verismo',
            'missione_visione',
            'comitato_tecnico_scientifico',
            'comitato_regolamento',
            'partner_rete_territoriale',
            'regolamenti_documenti',
            'vizzini',
            'licodia',
            'mineo',
            'privacy_policy',
            'cookie_policy',
            'note_legali',

        ]

    def location(self, item):
        return reverse(item)


class OperaSitemap(Sitemap):
    """Sitemap per le opere letterarie"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Opera.objects.all()

    def lastmod(self, obj):
        # Le opere non hanno data di modifica, usa None
        return None


class AutoreSitemap(Sitemap):
    """Sitemap per le pagine degli autori"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Autore.objects.all()

    def location(self, obj):
        return reverse('opere_per_autore', kwargs={'autore_slug': obj.slug})


class EventoSitemap(Sitemap):
    """Sitemap per gli eventi"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Evento.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.data_inizio


class NotiziaSitemap(Sitemap):
    """Sitemap per le notizie"""
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Notizia.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.data_pubblicazione


class DocumentoSitemap(Sitemap):
    """Sitemap per i documenti e studi"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Documento.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.data_pubblicazione


class ItinerarioSitemap(Sitemap):
    """Sitemap per gli itinerari"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Itinerario.objects.filter(is_active=True)

    def lastmod(self, obj):
        # Gli itinerari non hanno data di modifica
        return None
