"""
Admin per Documenti e Archivio Fotografico.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Documento, FotoArchivio
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html


@admin.register(Documento)
class DocumentoAdmin(TranslatableAdmin):
    list_display = (
        "__str__",
        "tipo",
        "autori",
        "anno_pubblicazione",
        "data_pubblicazione",
        "is_active",
    )
    list_filter = ("is_active", "tipo", "anno_pubblicazione", "data_pubblicazione")
    search_fields = ("translations__titolo", "translations__descrizione", "autori")
    date_hierarchy = "data_pubblicazione"
    ordering = ("-data_pubblicazione",)
    list_editable = ("is_active",)
    fieldsets = (
        (None, {"fields": ("slug", "tipo", "is_active")}),
        (
            "Contenuto",
            {"fields": ("titolo", "descrizione", "riassunto", "parole_chiave")},
        ),
        ("File e Media", {"fields": ("pdf_file", "anteprima")}),
        ("Informazioni", {"fields": ("autori", "anno_pubblicazione")}),
    )


@admin.register(FotoArchivio)
class FotoArchivioAdmin(TranslatableAdmin):
    list_display = (
        "__str__",
        "autore",
        "categoria",
        "ordine",
        "data_aggiunta",
        "is_active",
    )
    list_filter = ("is_active", "autore", "categoria", "data_aggiunta")
    search_fields = ("translations__titolo", "translations__descrizione", "categoria")
    date_hierarchy = "data_aggiunta"
    ordering = ("ordine", "-data_aggiunta")
    list_editable = ("ordine", "is_active")
    fieldsets = (
        (None, {"fields": ("immagine", "autore", "categoria", "ordine", "is_active")}),
        ("Informazioni", {"fields": ("titolo", "descrizione")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # Solo in creazione
            form.base_fields['upload_multiple'] = forms.FileField(
                widget=forms.ClearableFileInput(attrs={'multiple': True}),
                required=False,
                label="Caricamento Multiplo",
                help_text="Seleziona più foto per caricarle tutte in una volta (ignora il campo 'Immagine' singolo)."
            )
            # Riorganizza i campi per mettere il caricamento multiplo in evidenza
            field_order = ['upload_multiple', 'immagine', 'autore', 'categoria', 'ordine', 'is_active', 'titolo', 'descrizione']
            # Nota: field_order non funziona sempre perfettamente con fieldsets, ma base_fields sì.
        return form

    def save_model(self, request, obj, form, change):
        # Se c'è un upload multiplo, gestiamo quello
        files = request.FILES.getlist('upload_multiple')
        
        if files and not change:  # Solo in creazione
            # Il primo file viene usato per l'oggetto corrente (che Django sta salvando)
            obj.immagine = files[0]
            if not obj.titolo:
                obj.titolo = files[0].name.split('.')[0]
            super().save_model(request, obj, form, change)
            
            # Gli altri file creano nuovi oggetti
            for f in files[1:]:
                FotoArchivio.objects.create(
                    immagine=f,
                    autore=obj.autore,
                    categoria=obj.categoria,
                    ordine=obj.ordine,
                    is_active=obj.is_active,
                    titolo=f.name.split('.')[0]
                )
        else:
            # Comportamento standard
            super().save_model(request, obj, form, change)
