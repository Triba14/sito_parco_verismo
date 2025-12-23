"""
Context processors per il Parco Letterario Giovanni Verga e Luigi Capuana.
Rendono disponibili variabili globali in tutti i template.
"""

from django.conf import settings


def google_analytics(request):
    """
    Passa il Google Analytics Measurement ID a tutti i template.
    """
    return {
        'GA_MEASUREMENT_ID': getattr(settings, 'GA_MEASUREMENT_ID', ''),
    }
