from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create superuser automatically"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "sternee2332006@gmail.com", "ANON77")
            self.stdout.write(self.style.SUCCESS("Superuser created"))
