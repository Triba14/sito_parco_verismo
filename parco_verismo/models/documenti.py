"""
Modelli per Documenti e Archivio Fotografico.
"""

# Django imports
from django.db import models
from django.urls import reverse

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields


class Documento(TranslatableModel):
    """
    Modello per documenti e studi pubblicati dal Parco Letterario.
    Solo gli admin possono creare e modificare questi documenti.
    """

    slug = models.SlugField(max_length=200, unique=True)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    anno_pubblicazione = models.IntegerField(
        null=True, blank=True, help_text="Anno di pubblicazione del documento/studio."
    )
    pdf_file = models.FileField(
        upload_to="documenti/pdf/", help_text="File PDF del documento o studio."
    )
    anteprima = models.ImageField(
        upload_to="documenti/anteprime/",
        blank=True,
        null=True,
        help_text="Immagine di anteprima del documento (copertina o prima pagina).",
    )
    is_active = models.BooleanField(
        default=True, help_text="Se il documento è attivo e visibile."
    )
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("documento", "Documento"),
            ("studio", "Studio"),
            ("ricerca", "Ricerca"),
            ("saggio", "Saggio"),
        ],
        default="documento",
        help_text="Tipo di documento/studio.",
    )
    autori = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Autori del documento/studio (es: 'Mario Rossi, Luigi Bianchi').",
    )

    translations = TranslatedFields(
        titolo=models.CharField(
            max_length=200, help_text="Titolo del documento o studio."
        ),
        descrizione=models.TextField(
            help_text="Descrizione dettagliata del contenuto del documento."
        ),
        riassunto=models.TextField(
            blank=True, null=True, help_text="Riassunto breve per le liste (opzionale)."
        ),
        parole_chiave=models.CharField(
            max_length=300,
            blank=True,
            null=True,
            help_text="Parole chiave separate da virgola (opzionale).",
        ),
    )

    class Meta:
        ordering = ["-data_pubblicazione"]
        verbose_name = "Documento"
        verbose_name_plural = "Documenti e Studi"

    def __str__(self):
        return self.safe_translation_getter("titolo", any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse("documento_detail", kwargs={"slug": self.slug})


class FotoArchivio(TranslatableModel):
    """
    Modello per le foto dell'archivio fotografico.
    Solo gli admin possono aggiungere foto.
    """

    immagine = models.ImageField(
        upload_to="archivio_fotografico/", help_text="Carica la foto per l'archivio."
    )
    data_aggiunta = models.DateTimeField(auto_now_add=True)
    ordine = models.IntegerField(
        default=0, help_text="Ordine di visualizzazione (numero più basso = prima)."
    )
    is_active = models.BooleanField(
        default=True, help_text="Se la foto è attiva e visibile."
    )

    AUTORE_CHOICES = [
        ("VERGA", "Giovanni Verga"),
        ("CAPUANA", "Luigi Capuana"),
        ("ALTRO", "Altro/Generico"),
    ]

    autore = models.CharField(
        max_length=20,
        choices=AUTORE_CHOICES,
        default="ALTRO",
        help_text="Seleziona l'autore a cui appartiene questa foto.",
    )

    categoria = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Categoria della foto (es: 'Luoghi', 'Eventi', 'Personaggi').",
    )

    translations = TranslatedFields(
        titolo=models.CharField(
            max_length=200,
            blank=True,
            null=True,
            help_text="Titolo della foto (opzionale).",
        ),
        descrizione=models.TextField(
            blank=True, null=True, help_text="Descrizione della foto (opzionale)."
        ),
    )

    class Meta:
        ordering = ["ordine", "-data_aggiunta"]
        verbose_name = "Foto Archivio"
        verbose_name_plural = "Archivio Fotografico"

    def __str__(self):
        titolo = self.safe_translation_getter("titolo", any_language=True)
        if titolo:
            return titolo
        return f"Foto #{self.pk}"
