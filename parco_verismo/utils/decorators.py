"""
Decoratori custom per il progetto.
"""

from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse


def cache_page_custom(timeout=300, key_prefix="view"):
    """
    Decoratore per cachare una view per un tempo specifico.

    Args:
        timeout: Tempo in secondi
        key_prefix: Prefisso per la chiave di cache
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Costruisci chiave cache
            cache_key = f"{key_prefix}:{request.path}:{request.GET.urlencode()}"

            # Prova a recuperare dalla cache
            response = cache.get(cache_key)
            if response is not None:
                return response

            # Se non in cache, esegui la view
            response = view_func(request, *args, **kwargs)

            # Salva in cache
            cache.set(cache_key, response, timeout)

            return response

        return wrapper

    return decorator


def require_ajax(view_func):
    """
    Decoratore che richiede che la richiesta sia AJAX.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse("Bad Request", status=400)
        return view_func(request, *args, **kwargs)

    return wrapper
