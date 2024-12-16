import json
import os
from django.core.management.base import BaseCommand
from myApp.models import Room

class Command(BaseCommand):
    help = 'Importă datele despre săli dintr-un fișier JSON'

    def handle(self, *args, **kwargs):
        # Specifică calea completă a fișierului JSON
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_json', 'room.json')
        file_path = os.path.abspath(file_path)

        # Deschide fișierul JSON
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fișierul JSON nu a fost găsit: {file_path}"))
            return

        for item in data:
            # Extrage datele din JSON
            json_id = item.get('id')
            name = item.get('name')
            short_name = item.get('shortName', '').strip()
            building_name = item.get('buildingName', '').strip()

            # Validări de bază
            if not json_id or json_id == "0":
                self.stdout.write(self.style.WARNING(f"Inregistrare cu ID invalid ignorată: {item}"))
                continue

            if not name or not short_name:
                self.stdout.write(self.style.WARNING(f"Informații incomplete pentru înregistrare: {item}"))
                continue

            # Creează sau actualizează sala
            room, created = Room.objects.update_or_create(
                id=json_id,  # Setăm ID-ul din JSON
                defaults={
                    'name': name,
                    'short_name': short_name,
                    'building_name': building_name,
                }
            )

            # Mesaje pentru succes/actualizare
            if created:
                self.stdout.write(self.style.SUCCESS(f"Sala {room.short_name} ({room.building_name}) cu ID {room.id} a fost creată."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Sala {room.short_name} ({room.building_name}) cu ID {room.id} a fost actualizată."))
