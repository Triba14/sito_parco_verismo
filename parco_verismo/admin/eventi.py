"""
Admin per Eventi e Notizie.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Evento, Notizia, EventoImage, NotiziaImage
from django import forms


class EventoImageInline(admin.TabularInline):
    model = EventoImage
    extra = 1


class NotiziaImageInline(admin.TabularInline):
    model = NotiziaImage
    extra = 1


@admin.register(Evento)
class EventoAdmin(TranslatableAdmin):
    list_display = ("__str__", "data_inizio", "data_fine", "is_active")
    list_filter = ("is_active", "data_inizio")
    search_fields = ("translations__titolo", "translations__luogo")
    date_hierarchy = "data_inizio"
    ordering = ("-data_inizio",)
    list_editable = ("is_active",)
    inlines = [EventoImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Aggiungiamo il campo dinamicamente per evitare di creare una classe Form separata
        form.base_fields['nuove_foto_galleria'] = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}),
            required=False,
            help_text="Seleziona più foto da aggiungere alla galleria."
        )
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = request.FILES.getlist('nuove_foto_galleria')
        for f in files:
            EventoImage.objects.create(evento=obj, immagine=f)


@admin.register(Notizia)
class NotiziaAdmin(TranslatableAdmin):
    list_display = ("__str__", "data_pubblicazione", "is_active")
    list_filter = ("is_active", "data_pubblicazione")
    search_fields = ("translations__titolo", "translations__contenuto")
    date_hierarchy = "data_pubblicazione"
    ordering = ("-data_pubblicazione",)
    list_editable = ("is_active",)
    inlines = [NotiziaImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['nuove_foto_galleria'] = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}),
            required=False,
            help_text="Seleziona più foto da aggiungere alla galleria."
        )
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = request.FILES.getlist('nuove_foto_galleria')
        for f in files:
            NotiziaImage.objects.create(notizia=obj, immagine=f)
