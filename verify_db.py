import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from parco_verismo.models import Autore, Opera, LuogoLetterario, OperaInLuogo, Evento, Notizia, FotoArchivio, Itinerario

print('--- VERIFICA DATABASE ---')
print(f'Autori: {Autore.objects.count()}')
for a in Autore.objects.all():
    print(f'  - {a.nome} (slug: {a.slug})')

print(f'\nOpere: {Opera.objects.count()}')
print(f'  - Verga: {Opera.objects.filter(autore__slug="giovanni-verga").count()}')
print(f'  - Capuana: {Opera.objects.filter(autore__slug="luigi-capuana").count()}')
first_opera = Opera.objects.first()
if first_opera:
    print(f'  Example: {first_opera.titolo} (Link: {first_opera.link_fonte})')

print(f'\nLuoghi: {LuogoLetterario.objects.count()}')
for l in LuogoLetterario.objects.all():
    print(f'  - {l.nome}')

print(f'\nAssociazioni Opera-Luogo: {OperaInLuogo.objects.count()}')
print(f'Eventi: {Evento.objects.count()}')
print(f'Notizie: {Notizia.objects.count()}')
print(f'Foto Archivio: {FotoArchivio.objects.count()}')
print(f'Itinerari: {Itinerario.objects.count()}')
