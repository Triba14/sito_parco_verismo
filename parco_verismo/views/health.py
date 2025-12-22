"""
Views di utilità per il sistema.
"""

from django.http import JsonResponse, HttpResponse


def health_check_view(request):
    """
    Endpoint di health check per Docker e Nginx.
    Utilizzato per verificare che l'applicazione sia in esecuzione.
    """
    return JsonResponse({
        "status": "healthy",
        "service": "parco-verismo",
    })


def google_verification_view(request):
    """
    Serve il file di verifica per Google Search Console.
    """
    return HttpResponse(
        "google-site-verification: googlebff3b6f1bd148bc7.html",
        content_type="text/html"
    )
