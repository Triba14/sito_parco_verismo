from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields

LUOGO_CHOICES = [
    ('mineo', 'Mineo'),
    ('licodia-eubea', 'Licodia Eubea'),
    ('vizzini', 'Vizzini'),
]

class Ristorante(TranslatableModel):
    slug = models.SlugField(_("Slug"), max_length=200, unique=True, blank=True, help_text=_("Lascia vuoto per generare automaticamente dal nome."))
    luogo = models.CharField(_("Luogo"), max_length=20, choices=LUOGO_CHOICES, blank=True, default='')
    logo = models.ImageField(_("Logo/Icona"), upload_to='ristoranti/loghi/', blank=True, null=True)
    numeri = models.CharField(_("Numeri di telefono"), max_length=100)
    link_maps = models.URLField(_("Link Google Maps"), max_length=500, blank=True, null=True)
    menu = models.ImageField(_("Menu (Immagine)"), upload_to='ristoranti/menu/')
    
    translations = TranslatedFields(
        nome=models.CharField(_("Nome Ristorante"), max_length=200),
        tipo=models.CharField(_("Tipo di Ristorante"), max_length=100, blank=True),
        indirizzo=models.CharField(_("Indirizzo"), max_length=255),
    )
    
    class Meta:
        verbose_name = _("Ristorante")
        verbose_name_plural = _("Ristoranti")

    def __str__(self):
        return self.safe_translation_getter("nome", any_language=True) or str(self.pk)

    def save(self, *args, **kwargs):
        if not self.slug:
            nome = self.safe_translation_getter('nome', any_language=True) or "ristorante"
            base_slug = slugify(nome)
            slug = base_slug
            counter = 1
            while Ristorante.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
