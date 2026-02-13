from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

class Ristorante(models.Model):
    nome = models.CharField(_("Nome Ristorante"), max_length=200)
    slug = AutoSlugField(populate_from='nome', unique=True)
    logo = models.ImageField(_("Logo/Icona"), upload_to='ristoranti/loghi/', blank=True, null=True)
    indirizzo = models.CharField(_("Indirizzo"), max_length=255)
    numeri = models.CharField(_("Numeri di telefono"), max_length=100)
    menu = models.ImageField(_("Menu (Immagine)"), upload_to='ristoranti/menu/')
    
    class Meta:
        verbose_name = _("Ristorante")
        verbose_name_plural = _("Ristoranti")
        ordering = ['nome']

    def __str__(self):
        return self.nome
