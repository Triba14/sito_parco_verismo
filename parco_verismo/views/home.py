"""
Views per la homepage.
"""

# Django imports
import logging
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

# Local imports
from ..forms.richiesta import RichiestaForm
from ..models import Evento, Notizia


def home_view(request):
    """Vista homepage con modulo di contatto e contenuti in evidenza."""
    # Gestione form di contatto con validazione
    if request.method == "POST":
        form = RichiestaForm(request.POST)
        if form.is_valid():
            try:
                richiesta = form.save()
                logging.info(
                    "Richiesta creata id=%s email=%s",
                    getattr(richiesta, "id", "unknown"),
                    richiesta.email,
                )
                messages.success(
                    request,
                    "Messaggio inviato con successo! Ti contatteremo al più presto via email.",
                )
                from django.urls import reverse
                from django.http import HttpResponseRedirect

                return HttpResponseRedirect(reverse("home") + "#richiesta-contatto")
            except Exception:
                logging.exception("Errore nel salvataggio della richiesta")
                messages.error(request, "Errore nel salvataggio. Riprova più tardi.")
        else:
            # Mostra errori di validazione
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f"{field_label}: {error}")
    else:
        form = RichiestaForm()

    # Eventi: prendere i prossimi eventi attivi (a partire da oggi) ordinati per data
    eventi_latest = Evento.objects.filter(
        is_active=True, data_inizio__gte=timezone.now()
    ).order_by("data_inizio")[:4]

    # Notizie: prendere le ultime notizie attive ordinate per data di pubblicazione
    notizie_latest = Notizia.objects.filter(is_active=True).order_by(
        "-data_pubblicazione"
    )[:4]

    context = {
        "eventi": eventi_latest,
        "notizie": notizie_latest,
        "oggi": timezone.now().date().isoformat(),
        "form": form,
    }
    return render(request, "parco_verismo/index.html", context)
