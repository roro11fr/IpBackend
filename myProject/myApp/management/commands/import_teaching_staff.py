# import json
# from django.contrib.auth.hashers import make_password
# from django.core.management.base import BaseCommand
# from myApp.models import TeachingStaff, CustomUser, Department, Faculty
# import os

# class Command(BaseCommand):
#     help = 'Importă datele profesorilor dintr-un fișier JSON și creează utilizatori și departamente'

#     def handle(self, *args, **kwargs):
#         # Specifică calea completă a fișierului JSON
#         file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_json', 'cadru.json')
#         file_path = os.path.abspath(file_path)
        
#         # Deschide fișierul JSON
#         with open(file_path, 'r') as f:
#             data = json.load(f)

#         for item in data:
#             # Extrage datele din JSON
#             last_name = (item.get('lastName') or '').strip()
#             first_name = (item.get('firstName') or '').strip()
#             email_address = (item.get('emailAddress') or '').strip()
#             phone_number = (item.get('phoneNumber') or '').strip()  # Opțional
#             faculty_name = (item.get('facultyName') or '').strip()
#             department_name = (item.get('departmentName') or '').strip()

#             # Dacă emailAddress este gol, creăm un email fals
#             if not email_address:
#                 email_address = f"{first_name.lower()}.{last_name.lower()}@example.com"
            
#             # Verificăm dacă email-ul există deja în baza de date
#             if CustomUser.objects.filter(username=email_address).exists():
#                 self.stdout.write(self.style.WARNING(f"Email duplicat pentru {first_name} {last_name}. Salt acest profesor."))
#                 continue  # Saltă acest profesor dacă există deja

#             # Setează rolul utilizatorului în funcție de facultate și departament
#             if not faculty_name or department_name == "Exterior":
#                 role = 'Other'
#             else:
#                 role = 'Professor'

#             # Căutăm facultatea pe baza numelui
#             faculty = Faculty.objects.filter(long_name=faculty_name).first()

#             # Dacă facultatea nu există, o creăm
#             if not faculty:
#                 faculty = Faculty.objects.create(long_name=faculty_name, short_name=faculty_name[:50])  # Folosim long_name ca short_name dacă nu există

#             # Creează sau găsește departamentul
#             department, created = Department.objects.get_or_create(
#                 name=department_name,
#                 faculty_name=faculty_name  # Aici poate fi folosit și facultatea
#             )

#             # Crează utilizatorul CustomUser
#             custom_user = CustomUser.objects.create(
#                 username=email_address,  # Folosim email-ul ca username
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email_address,
#                 role=role,  # Setează rolul la Profesor sau Other
#                 status='Active',  # Statusul este Active
#                 password=make_password(f"cadru{item.get('id', '')}")  # Crează parola: cadru{id} sau o valoare alternativă
#             )

#             # Creează obiectul TeachingStaff
#             teaching_staff = TeachingStaff.objects.create(
#                 user=custom_user,  # Leagă TeachingStaff de CustomUser
#                 department=department,  # Leagă TeachingStaff de Departament
#             )

#             # Actualizează facultatea departamentului
#             department.faculty = faculty  # Asociază facultatea corectă departamentului
#             department.save()

#             self.stdout.write(self.style.SUCCESS(f"Profesorul {first_name} {last_name} a fost importat cu succes"))

# import json
# from django.core.management.base import BaseCommand
# from myApp.models import Department, Faculty
# import os

# class Command(BaseCommand):
#     help = 'Actualizează departamentele cu facultățile corespunzătoare pe baza numelui facultății din JSON'

#     def handle(self, *args, **kwargs):
#         # Specifică calea completă a fișierului JSON
#         file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_json', 'cadru.json')
#         file_path = os.path.abspath(file_path)
        
#         # Deschide fișierul JSON
#         with open(file_path, 'r') as f:
#             data = json.load(f)

#         for item in data:
#             # Extrage facultatea și departamentul din JSON
#             faculty_name = (item.get('facultyName') or '').strip()
#             department_name = (item.get('departmentName') or '').strip()

#             # Căutăm facultatea pe baza long_name (sau short_name dacă preferi)
#             faculty = Faculty.objects.filter(long_name=faculty_name).first()

#             if not faculty:
#                 self.stdout.write(self.style.ERROR(f"Facultatea '{faculty_name}' nu a fost găsită."))
#                 continue

#             # Căutăm departamentul pe baza numelui
#             department = Department.objects.filter(name=department_name).first()

#             if not department:
#                 self.stdout.write(self.style.ERROR(f"Departamentul '{department_name}' nu a fost găsit."))
#                 continue

#             # Actualizăm faculty_id în tabelul Department
#             department.faculty = faculty  # actualizează referința la obiectul de tip Faculty
#             department.save()

#             self.stdout.write(self.style.SUCCESS(
#                 f"Departamentul '{department_name}' a fost actualizat cu facultatea '{faculty_name}' (ID: {faculty.id})."
#             ))


##
import json
import os
from django.core.management.base import BaseCommand
from myApp.models import TeachingStaff, CustomUser, Department


class Command(BaseCommand):
    help = 'Populează tabelul TeachingStaff cu ID-uri și legături corecte utilizând datele din JSON'

    def handle(self, *args, **kwargs):
        # Specifică calea completă a fișierului JSON
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_json', 'cadru.json')
        file_path = os.path.abspath(file_path)

        # Încearcă să deschidă fișierul JSON
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fișierul JSON nu a fost găsit: {file_path}"))
            return

        for item in data:
            # Preia datele din JSON
            json_id = int(item.get('id', 0))
            email_address = (item.get('emailAddress') or '').strip().lower()
            phone_number = (item.get('phoneNumber') or '').strip()
            department_name = (item.get('departmentName') or '').strip()

            # Verifică validitatea ID-ului din JSON
            if json_id <= 0:
                self.stdout.write(self.style.WARNING(f"Înregistrare cu ID invalid ignorată: {item}"))
                continue

            try:
                # Căutăm utilizatorul CustomUser pe baza email-ului
                custom_user = CustomUser.objects.get(email=email_address)
            except CustomUser.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f"Există mai mulți utilizatori cu același email: {email_address}."))
                # Tipărim toate email-urile care corespund pentru a verifica duplicatele
                users_with_email = CustomUser.objects.filter(email=email_address)
                for user in users_with_email:
                    self.stdout.write(self.style.WARNING(f"Utilizator găsit: {user.email} (ID: {user.id})"))
                # Folosim primul utilizator găsit
                custom_user = users_with_email.first()
                self.stdout.write(self.style.WARNING(f"Folosit primul utilizator găsit cu email {email_address}."))
            except CustomUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Utilizatorul cu email {email_address} nu a fost găsit."))
                continue

            # Căutăm departamentul pe baza numelui
            department = Department.objects.filter(name=department_name).first()
            if not department:
                self.stdout.write(self.style.WARNING(f"Departamentul '{department_name}' nu a fost găsit. Profesorul va fi creat fără departament."))

            # Verificăm dacă înregistrarea în TeachingStaff există deja
            teaching_staff, created = TeachingStaff.objects.update_or_create(
                user=custom_user,  # Verificăm unicitatea pe baza user_id
                defaults={
                    'id': json_id,  # Setăm ID-ul din JSON
                    'phone_number': phone_number,
                    'department': department  # Setăm departamentul găsit
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Profesorul {custom_user.first_name} {custom_user.last_name} (ID: {json_id}) a fost creat în TeachingStaff."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Profesorul {custom_user.first_name} {custom_user.last_name} (ID: {json_id}) a fost actualizat în TeachingStaff."))





