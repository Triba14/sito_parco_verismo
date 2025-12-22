"""
Modelli per Itinerari e Tappe.
"""

# Django imports
from django.db import models
from django.urls import reverse

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields


class Itinerario(TranslatableModel):
    """
    Modello per gli itinerari verghiani e capuaniani.
    """

    slug = models.SlugField(max_length=200, unique=True)
    immagine = models.ImageField(
        upload_to="itinerari/immagini/",
        help_text="Immagine rappresentativa dell'itinerario.",
    )
    link_maps = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link al percorso su Google Maps (opzionale)",
    )
    # Campi per la mappa interattiva
    coordinate_tappe = models.JSONField(
        blank=True,
        null=True,
        help_text=(
            "JSON con le coordinate delle tappe: "
            "[{'nome': 'Tappa 1', 'coords': [lat, lng], 'descrizione': '...', 'order': 1}, ...]"
        ),
    )
    colore_percorso = models.CharField(
        max_length=7,
        default="#2E7D32",
        help_text="Colore del percorso sulla mappa (formato hex, es: #2E7D32)",
    )
    icona_percorso = models.CharField(
        max_length=10,
        default="📖",
        help_text="Emoji/icona per il percorso (es: 📖, 🏛️, 🍷)",
    )
    durata_stimata = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Durata stimata (es: '2-3 ore', 'Mezza giornata')",
    )
    difficolta = models.CharField(
        max_length=50,
        choices=[
            ("facile", "Facile"),
            ("media", "Media"),
            ("difficile", "Difficile"),
        ],
        default="facile",
        help_text="Difficoltà del percorso",
    )
    ordine = models.IntegerField(
        default=0, help_text="Ordine di visualizzazione (numero più basso = prima)."
    )
    is_active = models.BooleanField(
        default=True, help_text="Se l'itinerario è attivo e visibile."
    )
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("verghiano", "Itinerario Verghiano"),
            ("capuaniano", "Itinerario Capuaniano"),
            ("tematico", "Itinerario Tematico"),
        ],
        default="verghiano",
        help_text="Tipo di itinerario.",
    )

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200, help_text="Titolo dell'itinerario."),
        descrizione=models.TextField(
            help_text="Descrizione dettagliata dell'itinerario."
        ),
    )

    class Meta:
        ordering = ["ordine", "slug"]
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerari"

    def __str__(self):
        return self.safe_translation_getter("titolo", any_language=True) or str(self.pk)

    def get_absolute_url(self):
        """Return the detail URL for this itinerario."""
        return reverse("itinerario_detail", kwargs={"slug": self.slug})


class TappaItinerario(TranslatableModel):
    """
    Modello per le singole tappe di un itinerario.
    """

    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,
        related_name="tappe",
        help_text="Itinerario a cui appartiene questa tappa.",
    )
    ordine = models.IntegerField(
        default=0,
        help_text="Ordine della tappa nell'itinerario (numero più basso = prima).",
    )
    immagine = models.ImageField(
        upload_to="itinerari/tappe/",
        blank=True,
        null=True,
        help_text="Immagine rappresentativa della tappa (opzionale).",
    )

    translations = TranslatedFields(
        nome=models.CharField(
            max_length=200,
            help_text="Nome della tappa (es. 'Tappa 1: Chiesa di Santa Margherita')",
        ),
        descrizione=models.TextField(help_text="Descrizione dettagliata della tappa."),
    )

    class Meta:
        ordering = ["ordine"]
        verbose_name = "Tappa Itinerario"
        verbose_name_plural = "Tappe Itinerari"

    def __str__(self):
        nome = self.safe_translation_getter("nome", any_language=True)
        itinerario_nome = (
            self.itinerario.safe_translation_getter("titolo", any_language=True)
            if self.itinerario
            else "N/A"
        )
        return f"{itinerario_nome} - {nome}" if nome else f"Tappa #{self.pk}"
