"""
Modelli per Autori e Opere letterarie.
"""
# Django imports
from django.db import models
from django.urls import reverse

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields


class Autore(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    # ... puoi aggiungere biografia, foto, etc.

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Autore"
        verbose_name_plural = "Autori"


class Opera(TranslatableModel):
    autore = models.ForeignKey(Autore, on_delete=models.PROTECT, related_name='opere')
    slug = models.SlugField(max_length=200, unique=True)
    anno_pubblicazione = models.IntegerField(null=True, blank=True, verbose_name="Anno di pubblicazione")
    link_wikisource = models.URLField(max_length=500, help_text="Link alla pagina dell'opera su Wikisource.")
    copertina = models.ImageField(upload_to="copertine/", blank=True, null=True, help_text="Carica la copertina dell'opera.")

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        breve_descrizione=models.TextField(blank=True, null=True, verbose_name="Breve descrizione"),
        trama=models.TextField(help_text="Breve trama o descrizione dell'opera.", verbose_name="Trama"),
        analisi=models.TextField(blank=True, null=True, help_text="Spunti di analisi o contesto storico.", verbose_name="Analisi e contesto"),
    )

    class Meta:
        ordering = ['anno_pubblicazione', 'slug']
        verbose_name = "Opera"
        verbose_name_plural = "Opere"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse('opera_detail', kwargs={'slug': self.slug})
