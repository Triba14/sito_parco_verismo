"""
Utility functions e helper per il progetto.
"""


def truncate_text(text, max_length=100, suffix="..."):
    """
    Tronca un testo alla lunghezza massima specificata.

    Args:
        text: Il testo da troncare
        max_length: Lunghezza massima
        suffix: Suffisso da aggiungere se il testo viene troncato

    Returns:
        Il testo troncato
    """
    if not text or len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def slugify_italian(text):
    """
    Crea uno slug da un testo italiano, gestendo le lettere accentate.

    Args:
        text: Il testo da convertire in slug

    Returns:
        Lo slug generato
    """
    from django.utils.text import slugify
    import unicodedata

    # Normalizza il testo rimuovendo gli accenti
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    return slugify(text)


def format_phone_number(phone):
    """
    Formatta un numero di telefono per la visualizzazione.

    Args:
        phone: Il numero di telefono da formattare

    Returns:
        Il numero formattato
    """
    if not phone:
        return ""

    # Rimuovi tutti i caratteri non numerici tranne il +
    import re

    cleaned = re.sub(r"[^\d+]", "", phone)

    # Formatta in base alla lunghezza
    if cleaned.startswith("+39"):
        # Numero italiano
        return f"+39 {cleaned[3:6]} {cleaned[6:9]} {cleaned[9:]}"

    return phone


def get_client_ip(request):
    """
    Ottiene l'IP reale del client considerando proxy e load balancer.

    Args:
        request: L'oggetto HttpRequest

    Returns:
        L'indirizzo IP del client
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
