from django.core.management.base import BaseCommand
from myApp.models import Request

class Command(BaseCommand):
    help = 'Șterge toate cererile cu statusul "Rejected"'

    def handle(self, *args, **kwargs):
        deleted_count, _ = Request.objects.filter(status="Rejected").delete()
        self.stdout.write(f"{deleted_count} cereri 'Rejected' au fost șterse.")
