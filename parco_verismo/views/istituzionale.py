"""
Views per pagine istituzionali e di conformità.
"""

# Django imports
from django.shortcuts import render


# =============================================================================
# VIEWS ISTITUZIONALI E INFORMATIVE
# =============================================================================


def missione_visione_view(request):
    """Pagina Missione e Visione del Parco Letterario."""
    return render(request, "parco_verismo/missione_visione.html")


def comitato_tecnico_scientifico_view(request):
    """Pagina del Comitato Tecnico-Scientifico del Parco Letterario."""
    return render(request, "parco_verismo/comitato_tecnico_scientifico.html")


def comitato_regolamento_view(request):
    """Pagina del regolamento del Comitato Tecnico-Scientifico."""
    return render(request, "parco_verismo/comitato_regolamento.html")
def regolamenti_documenti_view(request):
    """Pagina Regolamenti e Documenti del Parco."""
    return render(request, "parco_verismo/regolamenti_documenti.html")


def partner_rete_territoriale_view(request):
    """Pagina Partner e Rete Territoriale."""
    return render(request, "parco_verismo/partner_rete_territoriale.html")


def accrediti_finanziamenti_view(request):
    """Pagina Accrediti e Finanziamenti."""
    return render(request, "parco_verismo/accrediti_finanziamenti.html")


def contatti_view(request):
    """Pagina Contatti del Parco Letterario."""
    return render(request, "parco_verismo/contatti.html")


# =============================================================================
# VIEWS PER CONFORMITÀ GDPR E PA
# =============================================================================


def privacy_policy_view(request):
    """Pagina Privacy Policy conforme GDPR."""
    return render(request, "parco_verismo/privacy_policy.html")


def note_legali_view(request):
    """Pagina Note Legali per PA."""
    return render(request, "parco_verismo/note_legali.html")


def cookie_policy_view(request):
    """Pagina Cookie Policy."""
    return render(request, "parco_verismo/cookie_policy.html")
