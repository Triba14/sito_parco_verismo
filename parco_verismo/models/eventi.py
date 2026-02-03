"""
Modelli per Eventi e Notizie.
"""

# Django imports
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from parler.models import TranslatableModel, TranslatedFields
from parco_verismo.utils.image_optimizer import optimize_image


class Evento(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="Lascia vuoto per generare automaticamente dal titolo.")
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

    def save(self, *args, **kwargs):
        if not self.slug:
            titolo = self.safe_translation_getter('titolo', any_language=True) or "evento"
            base_slug = slugify(titolo)
            slug = base_slug
            counter = 1
            while Evento.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Ottimizza l'immagine
        if self.immagine:
            try:
                this = Evento.objects.get(pk=self.pk)
                if this.immagine != self.immagine:
                    self.immagine = optimize_image(self.immagine)
            except Evento.DoesNotExist:
                self.immagine = optimize_image(self.immagine)
        
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        from django.utils import timezone

        return self.data_inizio < timezone.now()


class Notizia(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="Lascia vuoto per generare automaticamente dal titolo.")
    data_pubblicazione = models.DateTimeField(default=timezone.now)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            titolo = self.safe_translation_getter('titolo', any_language=True) or "notizia"
            base_slug = slugify(titolo)
            slug = base_slug
            counter = 1
            while Notizia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Ottimizza l'immagine
        if self.immagine:
            try:
                this = Notizia.objects.get(pk=self.pk)
                if this.immagine != self.immagine:
                    self.immagine = optimize_image(self.immagine)
            except Notizia.DoesNotExist:
                self.immagine = optimize_image(self.immagine)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("notizia_detail", kwargs={"slug": self.slug})


class EventoImage(models.Model):
    evento = models.ForeignKey(Evento, related_name='additional_images', on_delete=models.CASCADE)
    immagine = models.ImageField(upload_to="eventi/gallery/")
    didascalia = models.CharField(max_length=200, blank=True, null=True)
    ordine = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordine']
        verbose_name = "Immagine Evento"
        verbose_name_plural = "Immagini Evento"

    def save(self, *args, **kwargs):
        if self.immagine:
            try:
                this = EventoImage.objects.get(pk=self.pk)
                if this.immagine != self.immagine:
                    self.immagine = optimize_image(self.immagine)
            except EventoImage.DoesNotExist:
                self.immagine = optimize_image(self.immagine)
        super().save(*args, **kwargs)


class NotiziaImage(models.Model):
    notizia = models.ForeignKey(Notizia, related_name='additional_images', on_delete=models.CASCADE)
    immagine = models.ImageField(upload_to="notizie/gallery/")
    didascalia = models.CharField(max_length=200, blank=True, null=True)
    ordine = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordine']
        verbose_name = "Immagine Notizia"
        verbose_name_plural = "Immagini Notizia"

    def save(self, *args, **kwargs):
        if self.immagine:
            try:
                this = NotiziaImage.objects.get(pk=self.pk)
                if this.immagine != self.immagine:
                    self.immagine = optimize_image(self.immagine)
            except NotiziaImage.DoesNotExist:
                self.immagine = optimize_image(self.immagine)
        super().save(*args, **kwargs)


class EventoDocumento(models.Model):
    evento = models.ForeignKey(Evento, related_name='documenti', on_delete=models.CASCADE)
    file = models.FileField(upload_to="eventi/documenti/")
    titolo = models.CharField(max_length=200, help_text="Titolo descrittivo del documento")
    ordine = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordine']
        verbose_name = "Documento Evento"
        verbose_name_plural = "Documenti Evento"

    def __str__(self):
        return self.titolo


class NotiziaDocumento(models.Model):
    notizia = models.ForeignKey(Notizia, related_name='documenti', on_delete=models.CASCADE)
    file = models.FileField(upload_to="notizie/documenti/")
    titolo = models.CharField(max_length=200, help_text="Titolo descrittivo del documento")
    ordine = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordine']
        verbose_name = "Documento Notizia"
        verbose_name_plural = "Documenti Notizia"

    def __str__(self):
        return self.titolo
