
import os
import sys
import django

def diagnose():
    print("--- DIAGNOSTICA SITO PARCO VERISMO ---")
    
    # 1. Check Python Version
    print(f"Python: {sys.version}")
    
    # 2. Check Environment
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        django.setup()
        print("✅ Django Environment loaded successfully.")
    except Exception as e:
        print(f"❌ ERROR loading Django: {e}")
        return

    # 3. Check System Configuration
    from django.core.management import call_command
    try:
        call_command('check')
        print("✅ System Check passed.")
    except Exception as e:
        print(f"❌ System Check FAILED: {e}")
        return

    # 4. Check Migrations
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor
    try:
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        if plan:
            print(f"⚠️  WARNING: There are {len(plan)} unapplied migrations.")
            print("   Esegui: python manage.py migrate")
        else:
            print("✅ Database is up to date.")
    except Exception as e:
        print(f"❌ Database Check FAILED: {e}")

    print("\n--- CONCLUSIONE ---")
    print("Se vedi tutte spunte verdi qui sopra, il codice è corretto.")
    print("Il problema è probabilmente che il SERVER WEB non è stato riavviato.")
    print("Esegui: sudo systemctl restart gunicorn (o il comando appropriato per il tuo server).")

if __name__ == "__main__":
    diagnose()
