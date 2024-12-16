# management/commands/import_faculties.py
import json
from django.core.management.base import BaseCommand
from myApp.models import Faculty
import os

class Command(BaseCommand):
    help = 'Importă facultățile dintr-un fișier JSON'

    def handle(self, *args, **kwargs):
        # Specifică calea completă a fișierului JSON
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_json', 'faculty.json')
        file_path = os.path.abspath(file_path)

        # Deschide fișierul JSON
        with open(file_path, 'r') as f:
            data = json.load(f)

        for item in data:
            json_id = item.get('id')  # Extrage ID-ul din JSON
            short_name = item.get('shortName', '').strip()
            long_name = item.get('longName', '').strip()

            # Verifică dacă datele sunt valide
            if not json_id or not short_name or not long_name:
                self.stdout.write(self.style.WARNING(f"Date incomplete sau invalide pentru facultatea: {item}"))
                continue

            # Creează sau actualizează facultatea folosind ID-ul din JSON
            faculty, created = Faculty.objects.update_or_create(
                id=json_id,  # Folosește ID-ul din JSON pentru a căuta facultatea
                defaults={  # Dacă nu găsește facultatea, o creează cu long_name
                    'short_name': short_name,
                    'long_name': long_name
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Facultatea {short_name} (ID: {json_id}) a fost creată cu succes."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Facultatea {short_name} (ID: {json_id}) deja există."))
