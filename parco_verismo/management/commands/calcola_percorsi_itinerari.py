"""
Comando Django per calcolare e salvare i percorsi stradali degli itinerari.
Usa OSRM per calcolare i percorsi pedonali reali tra le tappe.
I percorsi vengono salvati nel database una sola volta.
"""

from django.core.management.base import BaseCommand
from parco_verismo.models import Itinerario
import requests
import time


class Command(BaseCommand):
    help = 'Calcola e salva i percorsi stradali per tutti gli itinerari'

    def handle(self, *args, **options):
        itinerari = Itinerario.objects.filter(is_active=True)
        
        self.stdout.write(f"\n{'='*70}")
        self.stdout.write(f"CALCOLO PERCORSI ITINERARI")
        self.stdout.write(f"{'='*70}\n")
        
        for itinerario in itinerari:
            self.stdout.write(f"\n📍 Itinerario: {itinerario.titolo}")
            self.stdout.write(f"   Tipo: {itinerario.get_tipo_display()}")
            
            if not itinerario.coordinate_tappe or len(itinerario.coordinate_tappe) < 2:
                self.stdout.write(self.style.WARNING(f"   ⚠ Saltato: meno di 2 tappe\n"))
                continue
            
            percorsi = {}
            totale_tappe = len(itinerario.coordinate_tappe)
            
            self.stdout.write(f"   Tappe totali: {totale_tappe}")
            self.stdout.write(f"   Percorsi da calcolare: {totale_tappe - 1}\n")
            
            for i in range(totale_tappe - 1):
                tappa_corrente = itinerario.coordinate_tappe[i]
                tappa_successiva = itinerario.coordinate_tappe[i + 1]
                
                start = tappa_corrente['coords']
                end = tappa_successiva['coords']
                
                nome_corrente = tappa_corrente.get('nome', f'Tappa {i+1}')
                nome_successiva = tappa_successiva.get('nome', f'Tappa {i+2}')
                
                self.stdout.write(f"   [{i+1}/{totale_tappe-1}] {nome_corrente} → {nome_successiva}")
                
                try:
                    # Chiama OSRM per il routing pedonale
                    url = (
                        f"https://router.project-osrm.org/route/v1/foot/"
                        f"{start[1]},{start[0]};{end[1]},{end[0]}"
                        f"?overview=full&geometries=geojson"
                    )
                    
                    self.stdout.write(f"       → Richiesta OSRM...", ending='')
                    self.stdout.flush()
                    
                    response = requests.get(url, timeout=15)
                    data = response.json()
                    
                    if data.get('code') == 'Ok' and data.get('routes'):
                        coords = data['routes'][0]['geometry']['coordinates']
                        # Converti [lng, lat] in [lat, lng] per Leaflet
                        coords_lat_lng = [[c[1], c[0]] for c in coords]
                        
                        distance = data['routes'][0]['distance']  # metri
                        duration = data['routes'][0]['duration']  # secondi
                        
                        percorsi[f"{i}_{i+1}"] = {
                            'coords': coords_lat_lng,
                            'distance': round(distance, 2),
                            'duration': round(duration, 2),
                            'tratteggiato': tappa_successiva.get('tratteggiato', False),
                            'punti': len(coords_lat_lng)
                        }
                        
                        self.stdout.write(self.style.SUCCESS(
                            f" ✓ ({len(coords_lat_lng)} punti, {distance:.0f}m, {duration/60:.1f}min)"
                        ))
                    else:
                        # Fallback a linea retta
                        percorsi[f"{i}_{i+1}"] = {
                            'coords': [start, end],
                            'straight_line': True,
                            'tratteggiato': tappa_successiva.get('tratteggiato', False)
                        }
                        error_code = data.get('code', 'unknown')
                        self.stdout.write(self.style.WARNING(
                            f" ⚠ Fallback linea retta (OSRM: {error_code})"
                        ))
                    
                    # Pausa per non sovraccaricare OSRM
                    time.sleep(0.6)
                    
                except requests.exceptions.Timeout:
                    self.stdout.write(self.style.ERROR(f" ✗ Timeout"))
                    percorsi[f"{i}_{i+1}"] = {
                        'coords': [start, end],
                        'straight_line': True,
                        'tratteggiato': tappa_successiva.get('tratteggiato', False)
                    }
                    
                except Exception as e:
                    error_msg = str(e)[:50]
                    self.stdout.write(self.style.ERROR(f" ✗ Errore: {error_msg}"))
                    percorsi[f"{i}_{i+1}"] = {
                        'coords': [start, end],
                        'straight_line': True,
                        'tratteggiato': tappa_successiva.get('tratteggiato', False)
                    }
            
            # Salva i percorsi nel database
            itinerario.percorsi_calcolati = percorsi
            itinerario.save()
            
            total_points = sum(p.get('punti', 2) for p in percorsi.values())
            total_distance = sum(p.get('distance', 0) for p in percorsi.values())
            
            self.stdout.write(self.style.SUCCESS(
                f"\n   ✓ SALVATO: {len(percorsi)} percorsi, "
                f"{total_points} punti, {total_distance:.0f}m totali\n"
            ))
        
        self.stdout.write(self.style.SUCCESS(f"\n{'='*70}"))
        self.stdout.write(self.style.SUCCESS(
            f"✓ COMPLETATO! Percorsi calcolati per {itinerari.count()} itinerari"
        ))
        self.stdout.write(self.style.SUCCESS(f"{'='*70}\n"))
