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
            short_name = item.get('shortName', '').strip()
            long_name = item.get('longName', '').strip()

            # Creează sau actualizează facultatea
            faculty, created = Faculty.objects.get_or_create(
                short_name=short_name,  # Folosește `short_name` pentru a căuta facultatea
                defaults={  # Dacă nu gaseste, creează o nouă facultate
                    'long_name': long_name
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Facultatea {short_name} a fost creată cu succes."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Facultatea {short_name} deja există."))
