"""
Mixins riutilizzabili per views e modelli.
"""

from django.contrib import messages


class FormSuccessMessageMixin:
    """
    Mixin che aggiunge un messaggio di successo dopo il salvataggio di un form.
    """

    success_message = "Operazione completata con successo!"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class ActiveOnlyMixin:
    """
    Mixin per filtrare solo oggetti attivi (is_active=True).
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


class TimestampMixin:
    """
    Mixin per aggiungere campi di timestamp ai modelli.
    Questo andrebbe aggiunto ai modelli base se necessario.
    """

    pass  # Placeholder per future implementazioni
