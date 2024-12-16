from django.core.management.base import BaseCommand
import random
from myApp.models import Request, CustomUser, Exam


class Command(BaseCommand):
    help = "Populează baza de date cu 10 request-uri random."

    def handle(self, *args, **kwargs):
        users = list(CustomUser.objects.all())
        exams = list(Exam.objects.all())

        if len(users) < 2 or len(exams) == 0:
            self.stdout.write("Asigură-te că ai cel puțin 2 utilizatori și examene în baza de date.")
        else:
            status_choices = ['Pending', 'Approved', 'Rejected']

            for _ in range(10):
                user = random.choice(users)
                destinatar = random.choice(users)

                # Evită ca user-ul și destinatarul să fie aceeași persoană
                while destinatar == user:
                    destinatar = random.choice(users)

                exam = random.choice(exams)
                status = random.choice(status_choices)

                # Creează obiectul Request
                Request.objects.create(
                    user=user,
                    destinatar=destinatar,
                    exam=exam,
                    status=status
                )

            self.stdout.write("10 request-uri random au fost adăugate în baza de date.")
