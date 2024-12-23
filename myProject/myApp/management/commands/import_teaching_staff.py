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
from myApp.models import CustomUser, TeachingStaff, Department, DepartmentHead

class Command(BaseCommand):
    help = 'Șterge utilizatorii cu ID>=17 și îi recreează conform datelor din JSON'

    def handle(self, *args, **kwargs):
        # Ștergem toți utilizatorii cu ID>=17
        CustomUser.objects.filter(id__gte=10, id__lte=17).delete()
        self.stdout.write(self.style.SUCCESS(f"Toți utilizatorii cu ID>=17 au fost șterși."))

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

            if json_id <= 0:
                self.stdout.write(self.style.WARNING(f"ID-ul din JSON nu este valid: {json_id}"))
                continue

            # Căutăm utilizatorul pe baza adresei de email
            try:
                # Creăm utilizatorul conform datelor din JSON
                new_user = CustomUser.objects.create(
                    id=json_id,  # Setăm ID-ul din JSON
                    username=email_address,  # Username-ul este același cu email-ul
                    email=email_address,
                    first_name=item.get('firstName', ''),
                    last_name=item.get('lastName', ''),
                    password='cadru',  # Setează o parolă standard pentru toți utilizatorii
                    role=item.get('role', 'Professor'),  # Dacă există un câmp 'role' în JSON
                    status='Active'  # Setăm statusul activ
                )

                # Setăm parola noului utilizator
                new_user.set_password('cadru')  # Setează o parolă dacă este necesar
                new_user.save()

                self.stdout.write(self.style.SUCCESS(f"Utilizatorul {new_user.email} a fost creat cu ID-ul {json_id}."))

                # Căutăm departamentul pe baza numelui
                department = Department.objects.filter(name=department_name).first()
                if department:
                    self.stdout.write(self.style.SUCCESS(f"Departamentul '{department_name}' a fost găsit."))
                else:
                    self.stdout.write(self.style.WARNING(f"Departamentul '{department_name}' nu a fost găsit. Profesorul va fi creat fără departament."))

                # Creăm înregistrarea pentru TeachingStaff
                TeachingStaff.objects.create(
                    user=new_user,
                    phone_number=phone_number,
                    department=department  # Dacă departamentul a fost găsit, îl asociem
                )

                # Dacă există departament head, creăm înregistrarea pentru DepartmentHead
                if department:
                    DepartmentHead.objects.create(
                        user=new_user,
                        department=department
                    )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Eroare la crearea utilizatorului {email_address}: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS("Toți utilizatorii din JSON au fost creați cu succes!"))





