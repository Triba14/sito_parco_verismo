"""
Utility functions e helper del progetto.
"""

from .helpers import (
    truncate_text,
    slugify_italian,
    format_phone_number,
    get_client_ip,
)

from .decorators import (
    cache_page_custom,
    require_ajax,
)

from .mixins import (
    FormSuccessMessageMixin,
    ActiveOnlyMixin,
)

__all__ = [
    # Helpers
    "truncate_text",
    "slugify_italian",
    "format_phone_number",
    "get_client_ip",
    # Decorators
    "cache_page_custom",
    "require_ajax",
    # Mixins
    "FormSuccessMessageMixin",
    "ActiveOnlyMixin",
]
