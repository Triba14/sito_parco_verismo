from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

LUOGO_CHOICES = [
    ('mineo', 'Mineo'),
    ('licodia-eubea', 'Licodia Eubea'),
    ('vizzini', 'Vizzini'),
]

class Ristorante(models.Model):
    nome = models.CharField(_("Nome Ristorante"), max_length=200)
    tipo = models.CharField(_("Tipo di Ristorante"), max_length=100, blank=True)
    slug = AutoSlugField(populate_from='nome', unique=True)
    luogo = models.CharField(_("Luogo"), max_length=20, choices=LUOGO_CHOICES, blank=True, default='')
    logo = models.ImageField(_("Logo/Icona"), upload_to='ristoranti/loghi/', blank=True, null=True)
    indirizzo = models.CharField(_("Indirizzo"), max_length=255)
    numeri = models.CharField(_("Numeri di telefono"), max_length=100)
    link_maps = models.URLField(_("Link Google Maps"), max_length=500, blank=True, null=True)
    menu = models.ImageField(_("Menu (Immagine)"), upload_to='ristoranti/menu/')
    
    class Meta:
        verbose_name = _("Ristorante")
        verbose_name_plural = _("Ristoranti")
        ordering = ['nome']

    def __str__(self):
        return self.nome
