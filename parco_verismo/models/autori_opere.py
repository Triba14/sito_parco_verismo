"""
Modelli per Autori e Opere letterarie.
"""
# Django imports
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Third-party imports
from parler.models import TranslatableModel, TranslatedFields
from parco_verismo.utils.image_optimizer import optimize_image


class LuogoLetterario(models.Model):
    """Luoghi dell'ispirazione letteraria (Vizzini, Mineo, Licodia Eubea)"""
    nome = models.CharField(max_length=100, unique=True, verbose_name=_("Nome del luogo"))
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descrizione = models.TextField(blank=True, verbose_name=_("Descrizione"))
    ordine = models.IntegerField(default=0, help_text=_("Ordine di visualizzazione"))
    
    class Meta:
        verbose_name = _("Luogo Letterario")
        verbose_name_plural = _("Luoghi Letterari")
        ordering = ['ordine', 'nome']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            counter = 1
            while LuogoLetterario.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Autore(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text=_("Lascia vuoto per generare automaticamente dal nome."))
    # ... puoi aggiungere biografia, foto, etc.

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Genera slug automaticamente dal nome se non specificato
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            counter = 1
            while Autore.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Autore")
        verbose_name_plural = _("Autori")


class Opera(TranslatableModel):
    FONTE_CHOICES = [
        ('wikisource', _('WikiSource')),
        ('internet_archive', _('Internet Archive')),
        ('gutenberg', _('The Project Gutenberg')),
        ('altro', _('Altro')),
    ]
    
    autore = models.ForeignKey(Autore, on_delete=models.PROTECT, related_name='opere')
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text=_("Lascia vuoto per generare automaticamente dal titolo."))
    link_fonte = models.URLField(max_length=500, help_text=_("Link all'opera (WikiSource, Internet Archive, Gutenberg, etc.)"))
    fonte_testo = models.CharField(
        max_length=50,
        choices=FONTE_CHOICES,
        default='altro',
        blank=True,
        verbose_name=_("Fonte (opzionale)"),
        help_text=_("Lascia vuoto per rilevamento automatico dal link")
    )
    copertina = models.ImageField(upload_to="copertine/", blank=True, null=True, help_text=_("Carica la copertina dell'opera."))

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        breve_descrizione=models.TextField(blank=True, null=True, verbose_name=_("Breve descrizione")),
        trama=models.TextField(help_text=_("Breve trama o descrizione dell'opera."), verbose_name=_("Trama")),
        analisi=models.TextField(blank=True, null=True, help_text=_("Spunti di analisi o contesto storico."), verbose_name=_("Analisi e contesto")),
    )

    class Meta:
        ordering = ['slug']
        verbose_name = _("Opera")
        verbose_name_plural = _("Opere")

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Tenta di ottenere titolo (fallback a "opera" se vuoto)
            titolo = self.safe_translation_getter('titolo', any_language=True) or "opera"
            base_slug = slugify(titolo)
            slug = base_slug
            counter = 1
            while Opera.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Ottimizza l'immagine (copertina)
        if self.copertina:
            try:
                this = Opera.objects.get(pk=self.pk)
                if this.copertina != self.copertina:
                    self.copertina = optimize_image(self.copertina)
            except Opera.DoesNotExist:
                self.copertina = optimize_image(self.copertina)

        super().save(*args, **kwargs)
    
    def get_fonte_display_text(self):
        """Restituisce il testo completo da mostrare sul bottone"""
        # Se fonte_testo è impostato manualmente, usa quello
        if self.fonte_testo and self.fonte_testo != 'altro':
            fonte_map = {
                'wikisource': _("Leggi l'opera su WikiSource"),
                'internet_archive': _("Leggi l'opera su Internet Archive"),
                'gutenberg': _("Leggi l'opera su The Project Gutenberg"),
            }
            return fonte_map.get(self.fonte_testo, _("Leggi l'opera"))
        
        # Altrimenti, rileva automaticamente dal link
        link = self.get_link_esterno()
        if link:
            if 'wikisource.org' in link:
                return _("Leggi l'opera su WikiSource")
            elif 'archive.org' in link:
                return _("Leggi l'opera su Internet Archive")
            elif 'gutenberg.org' in link:
                return _("Leggi l'opera su The Project Gutenberg")
        
        return _("Leggi l'opera")
    
    def get_link_esterno(self):
        """Restituisce il link all'opera"""
        return self.link_fonte


class OperaInLuogo(models.Model):
    """Relazione molti-a-molti tra Opera e LuogoLetterario con categoria"""
    CATEGORIA_CHOICES = [
        ('romanzi', _('Romanzi')),
        ('novelle', _('Novelle')),
        ('teatro', _('Teatro')),
        ('fiabe', _('Fiabe')),
    ]
    
    opera = models.ForeignKey(Opera, on_delete=models.CASCADE, related_name='luoghi_opera', verbose_name=_("Opera"))
    luogo = models.ForeignKey(LuogoLetterario, on_delete=models.CASCADE, related_name='opere_luogo', verbose_name=_("Luogo"))
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        verbose_name=_("Categoria"),
        help_text=_("Categoria letteraria dell'opera in questo luogo")
    )
    ordine = models.IntegerField(default=0, verbose_name=_("Ordine"), help_text=_("Ordine di visualizzazione nella lista"))
    
    class Meta:
        verbose_name = _("Opera in Luogo")
        verbose_name_plural = _("Opere nei Luoghi")
        ordering = ['luogo__ordine', 'luogo__nome', 'categoria', 'ordine', 'opera__slug']
        unique_together = [['opera', 'luogo', 'categoria']]  # Stessa opera può essere in stesso luogo ma categorie diverse
    
    def __str__(self):
        opera_titolo = self.opera.safe_translation_getter('titolo', any_language=True) or str(self.opera.pk)
        return f"{opera_titolo} - {self.luogo.nome} ({self.get_categoria_display()})"

