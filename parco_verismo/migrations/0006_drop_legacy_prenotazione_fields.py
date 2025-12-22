# Generated manually: drop legacy columns from Prenotazione (now Richiesta)
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parco_verismo", "0005_richiesta_delete_prenotazione"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="richiesta",
            name="telefono",
        ),
        migrations.RemoveField(
            model_name="richiesta",
            name="luogo",
        ),
        migrations.RemoveField(
            model_name="richiesta",
            name="itinerario",
        ),
        migrations.RemoveField(
            model_name="richiesta",
            name="data_preferita",
        ),
        migrations.RemoveField(
            model_name="richiesta",
            name="numero_partecipanti",
        ),
    ]
