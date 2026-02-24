"""
Custom compilemessages command that automatically ignores .venv directory.

This overrides Django's built-in compilemessages to prevent it from scanning
the virtual environment, which causes spurious errors from Django's internal
.po files.

Usage (same as before, no extra flags needed):
    python manage.py compilemessages
    python manage.py compilemessages -l en
"""

from django.core.management.commands.compilemessages import (
    Command as BaseCommand,
)


class Command(BaseCommand):
    help = "Compiles .po files to .mo files (auto-ignores .venv)."

    def handle(self, *args, **options):
        # Always ignore .venv to avoid errors from Django's internal .po files
        ignore_patterns = list(options.get("ignore_patterns", []))
        if ".venv" not in ignore_patterns:
            ignore_patterns.append(".venv")
        options["ignore_patterns"] = ignore_patterns

        super().handle(*args, **options)
