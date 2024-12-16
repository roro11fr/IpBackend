from django.core.management.base import BaseCommand
from myApp.models import TeachingStaff, Professor

class Command(BaseCommand):
    help = 'Populează tabelul Professor din TeachingStaff'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populare Professor din TeachingStaff...")
        professors_created = 0

        for staff in TeachingStaff.objects.all():
            if Professor.objects.filter(user=staff.user).exists():
                continue

            Professor.objects.create(
                user=staff.user,
                department=staff.department,  # Folosim departamentul din TeachingStaff
                title="Titular",
                availability_start=None,
                availability_end=None,
                activity="Activitate didactica" 
            )
            professors_created += 1

        self.stdout.write(self.style.SUCCESS(f"{professors_created} înregistrări au fost adăugate în tabelul `Professor`."))
