"""
Middleware personalizzato per rate limiting e sicurezza.
"""

# Standard library imports
import time

# Django imports
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.translation import gettext as _


class SimpleRateLimitMiddleware:
    """
    Middleware semplice per rate limiting basato su IP
    Limita le richieste POST per prevenire spam e abusi

    Per siti con buona affluenza (consigliato):
    - 10 richieste POST per minuto per IP
    - 100 richieste GET per minuto per IP
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Configurazione rate limits
        self.limits = {
            "POST": {"requests": 10, "window": 60},  # 10 POST al minuto
            "GET": {"requests": 100, "window": 60},  # 100 GET al minuto
        }

    def __call__(self, request):
        # Salta il rate limiting per admin e static files
        if (
            request.path.startswith("/admin/")
            or request.path.startswith("/static/")
            or request.path.startswith("/media/")
        ):
            return self.get_response(request)

        # Ottieni IP del client
        ip_address = self.get_client_ip(request)
        method = request.method

        # Controlla rate limit solo per POST e GET
        if method in self.limits:
            if not self.check_rate_limit(ip_address, method):
                return HttpResponse(
                    _("Troppe richieste. Riprova tra qualche minuto."),
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Ottiene l'IP reale del client considerando proxy"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def check_rate_limit(self, ip_address, method):
        """Controlla se l'IP ha superato il rate limit"""
        limit_config = self.limits.get(method)
        if not limit_config:
            return True

        cache_key = f"ratelimit:{method}:{ip_address}"

        # Ottieni il contatore corrente
        request_times = cache.get(cache_key, [])
        current_time = time.time()
        window = limit_config["window"]
        max_requests = limit_config["requests"]

        # Rimuovi richieste fuori dalla finestra temporale
        request_times = [t for t in request_times if current_time - t < window]

        # Controlla se superato il limite
        if len(request_times) >= max_requests:
            return False

        # Aggiungi la richiesta corrente
        request_times.append(current_time)
        cache.set(cache_key, request_times, window)

        return True


class SecurityHeadersMiddleware:
    """
    Middleware per aggiungere header di sicurezza alle risposte
    Migliora la sicurezza del sito contro attacchi comuni
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Aggiungi security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "SAMEORIGIN"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy (adatta in base alle tue esigenze)
        # response['Content-Security-Policy'] = (
        #     "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        #     "style-src 'self' 'unsafe-inline'"
        # )

        return response
