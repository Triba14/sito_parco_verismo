"""
Modelli per Itinerari e Tappe - Sistema Rinnovato
"""

# Django imports
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields
from parco_verismo.utils.image_optimizer import optimize_image


class Itinerario(TranslatableModel):
    """
    Modello per gli itinerari letterari (Verghiani, Capuaniani, Tematici).
    Sistema completamente rinnovato con supporto per mappe interattive e tappe JSON.
    """
    
    # Campi base
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        help_text="Lascia vuoto per generare automaticamente dal titolo."
    )
    
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("verghiano", "Itinerario Verghiano"),
            ("capuaniano", "Itinerario Capuaniano"),
            ("tematico", "Itinerario Tematico"),
        ],
        default="verghiano",
        help_text="Tipo di itinerario letterario."
    )
    
    ordine = models.PositiveIntegerField(
        default=1, 
        help_text="Ordine di visualizzazione (numero più basso = prima posizione)."
    )
    
    # Media
    immagine = models.ImageField(
        upload_to="itinerari/",
        blank=True,
        null=True,
        help_text="Immagine di copertina dell'itinerario."
    )
    
    # Dettagli percorso
    durata_stimata = models.CharField(
        max_length=100,
        blank=True,
        help_text="Es: '2-3 ore', 'Mezza giornata', 'Intera giornata'"
    )
    
    difficolta = models.CharField(
        max_length=20,
        choices=[
            ("facile", "Facile"),
            ("medio", "Medio"),
            ("difficile", "Difficile"),
        ],
        default="facile",
        help_text="Livello di difficoltà del percorso"
    )
    
    # Coordinate e mappa
    coordinate_tappe = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            'Array JSON delle tappe: '
            '[{"nome": "Nome tappa", "coords": [lat, lng], "descrizione": "...", "order": 1}, ...]'
        )
    )
    
    percorsi_calcolati = models.JSONField(
        default=dict,
        blank=True,
        help_text="Percorsi stradali pre-calcolati tra le tappe (generati automaticamente)"
    )
    
    colore_percorso = models.CharField(
        max_length=7,
        default="#4A6741",
        help_text="Colore del percorso sulla mappa (hex, es: #4A6741)"
    )
    
    # Link esterno
    link_maps = models.URLField(
        max_length=500,
        blank=True,
        default='',
        help_text="Link al percorso su Google Maps (opzionale)"
    )
    
    # Pubblicazione
    is_active = models.BooleanField(
        default=True, 
        help_text="Se deselezionato, l'itinerario non sarà visibile sul sito."
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campi traducibili
    translations = TranslatedFields(
        titolo=models.CharField(
            max_length=200, 
            help_text="Titolo dell'itinerario."
        ),
        descrizione=models.TextField(
            help_text="Descrizione dettagliata dell'itinerario."
        ),
        note=models.TextField(
            blank=True,
            help_text="Note aggiuntive, informazioni pratiche, consigli."
        )
    )
    
    class Meta:
        ordering = ["tipo", "ordine"]
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerari"
        indexes = [
            models.Index(fields=["tipo", "ordine"]),
            models.Index(fields=["is_active"]),
        ]
    
    def __str__(self):
        return self.safe_translation_getter("titolo", any_language=True) or f"Itinerario {self.slug}"
    
    def save(self, *args, **kwargs):
        # Genera slug automaticamente dal titolo se non specificato
        if not self.slug:
            titolo = self.safe_translation_getter('titolo', any_language=True) or f'itinerario-{self.pk or "new"}'
            base_slug = slugify(titolo)
            slug = base_slug
            counter = 1
            while Itinerario.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Ottimizza l'immagine se presente e se è stata modificata (o è nuova)
        if self.immagine:
            # Controlliamo se è un nuovo file o se è cambiato
            try:
                this = Itinerario.objects.get(pk=self.pk)
                if this.immagine != self.immagine:
                    self.immagine = optimize_image(self.immagine)
            except Itinerario.DoesNotExist:
                # Se l'oggetto è nuovo
                self.immagine = optimize_image(self.immagine)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the detail URL for this itinerario."""
        return reverse("itinerario_detail", kwargs={"slug": self.slug})
    
    def get_centro_mappa(self):
        """Calcola il centro geografico delle tappe per centrare la mappa"""
        if not self.coordinate_tappe or not isinstance(self.coordinate_tappe, list):
            return [37.5, 14.7]  # Centro Sicilia default
        
        lats = [tappa['coords'][0] for tappa in self.coordinate_tappe if 'coords' in tappa and len(tappa['coords']) >= 2]
        lngs = [tappa['coords'][1] for tappa in self.coordinate_tappe if 'coords' in tappa and len(tappa['coords']) >= 2]
        
        if not lats or not lngs:
            return [37.5, 14.7]
        
        return [sum(lats) / len(lats), sum(lngs) / len(lngs)]
    
    def get_tappe_ordinate(self):
        """Restituisce le tappe ordinate per campo 'order'"""
        if not self.coordinate_tappe or not isinstance(self.coordinate_tappe, list):
            return []
        
        return sorted(self.coordinate_tappe, key=lambda x: x.get('order', 0))
    
    def get_numero_tappe(self):
        """Restituisce il numero di tappe"""
        if not self.coordinate_tappe or not isinstance(self.coordinate_tappe, list):
            return 0
        return len(self.coordinate_tappe)


class ItinerarioImmagine(models.Model):
    """
    Modello per le immagini della galleria di un itinerario.
    """
    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,
        related_name='galleria',
        verbose_name="Itinerario"
    )
    
    immagine = models.ImageField(
        upload_to='itinerari/galleria/',
        verbose_name="Immagine",
        help_text="Carica un'immagine per la galleria dell'itinerario"
    )
    
    ordine = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordine",
        help_text="Ordine di visualizzazione nel carosello"
    )
    
    didascalia = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Didascalia",
        help_text="Descrizione dell'immagine (opzionale)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordine', 'created_at']
        verbose_name = "Immagine Galleria"
        verbose_name_plural = "Immagini Galleria"
    
    def __str__(self):
        return f"{self.itinerario.titolo if hasattr(self.itinerario, 'titolo') else 'Itinerario'} - Immagine {self.ordine}"
