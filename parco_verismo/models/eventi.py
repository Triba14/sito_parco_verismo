"""
Modelli per Eventi e Notizie.
"""

# Django imports
from django.db import models
from django.urls import reverse

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields


class Evento(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True)
    data_inizio = models.DateTimeField(help_text="Data e ora di inizio dell'evento.")
    data_fine = models.DateTimeField(
        blank=True, null=True, help_text="Data e ora di fine dell'evento (opzionale)."
    )
    immagine = models.ImageField(
        upload_to="eventi/",
        blank=True,
        null=True,
        help_text="Immagine rappresentativa dell'evento.",
    )
    is_active = models.BooleanField(
        default=True, help_text="Se l'evento è attivo e visibile."
    )

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        descrizione=models.TextField(help_text="Descrizione dettagliata dell'evento."),
        luogo=models.CharField(
            max_length=200, help_text="Luogo dove si svolge l'evento."
        ),
        indirizzo=models.TextField(
            blank=True, null=True, help_text="Indirizzo completo del luogo."
        ),
    )

    class Meta:
        ordering = ["-data_inizio"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventi"

    def __str__(self):
        return self.safe_translation_getter("titolo", any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse("evento_detail", kwargs={"slug": self.slug})

    @property
    def is_past(self):
        from django.utils import timezone

        return self.data_inizio < timezone.now()


class Notizia(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    immagine = models.ImageField(
        upload_to="notizie/",
        blank=True,
        null=True,
        help_text="Immagine principale della notizia.",
    )
    is_active = models.BooleanField(
        default=True, help_text="Se la notizia è attiva e visibile."
    )

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        contenuto=models.TextField(help_text="Contenuto completo della notizia."),
        riassunto=models.TextField(
            blank=True, null=True, help_text="Riassunto breve per le liste (opzionale)."
        ),
    )

    class Meta:
        ordering = ["-data_pubblicazione"]
        verbose_name = "Notizia"
        verbose_name_plural = "Notizie"

    def __str__(self):
        return self.safe_translation_getter("titolo", any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse("notizia_detail", kwargs={"slug": self.slug})
