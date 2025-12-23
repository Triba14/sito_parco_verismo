"""
Servizi per la gestione delle email relative alle richieste.
"""

import logging
from django.core.mail import send_mail
from django.conf import settings


def invia_email_richiesta_confermata(richiesta):
    """
    Invia email di conferma al cliente dopo aver ricevuto la richiesta.

    Args:
        richiesta: Oggetto Richiesta

    Returns:
        True se l'email è stata inviata con successo, False altrimenti
    """
    try:
        subject = f"Richiesta ricevuta - {richiesta.oggetto or 'Richiesta contatto'}"

        # Crea il messaggio email
        # TODO: Creare template email quando necessario
        # message = render_to_string('emails/richiesta_confermata.html', {"richiesta": richiesta})

        message = f"""
        Gentile {richiesta.nome} {richiesta.cognome},

        Abbiamo ricevuto la tua richiesta.
        {f'- Ente: {richiesta.ente}' if richiesta.ente else ''}
        {f'- Oggetto: {richiesta.oggetto}' if richiesta.oggetto else ''}

        Ti contatteremo presto per rispondere alla tua richiesta.

        Cordiali saluti,
        Il Team del Parco Letterario Giovanni Verga e Luigi Capuana
        """

        send_mail(
            subject,
            message,
            (
                settings.DEFAULT_FROM_EMAIL
                if hasattr(settings, "DEFAULT_FROM_EMAIL")
                else "noreply@parcolettverismo.it"
            ),
            [richiesta.email],
            fail_silently=False,
        )

        return True
    except Exception:
        logging.exception(
            "Errore nell'invio email per richiesta id=%s",
            getattr(richiesta, "id", "unknown"),
        )
        return False


def invia_notifica_admin_nuova_richiesta(richiesta):
    """
    Invia una notifica agli amministratori quando arriva una nuova richiesta.

    Args:
        richiesta: Oggetto Richiesta

    Returns:
        True se l'email è stata inviata con successo, False altrimenti
    """
    try:
        subject = f"Nuova richiesta: {richiesta.nome} {richiesta.cognome} - {richiesta.oggetto or ''}"

        message = f"""
        Nuova richiesta ricevuta:

        Cliente: {richiesta.nome} {richiesta.cognome}
        Email: {richiesta.email}
        {f'Ente: {richiesta.ente}' if richiesta.ente else ''}
        {f'Oggetto: {richiesta.oggetto}' if richiesta.oggetto else ''}

        {f'Messaggio: {richiesta.messaggio}' if richiesta.messaggio else ''}

        Gestisci la richiesta dall'admin.
        """

        # TODO: Configurare ADMIN_EMAIL in settings
        admin_email = getattr(settings, "ADMIN_EMAIL", "admin@parcolettverismo.it")

        send_mail(
            subject,
            message,
            (
                settings.DEFAULT_FROM_EMAIL
                if hasattr(settings, "DEFAULT_FROM_EMAIL")
                else "noreply@parcolettverismo.it"
            ),
            [admin_email],
            fail_silently=False,
        )

        return True
    except Exception:
        logging.exception(
            "Errore nell'invio notifica admin per richiesta id=%s",
            getattr(richiesta, "id", "unknown"),
        )
        return False
