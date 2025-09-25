# rcnb/users/management/commands/test_command.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'A simple test command that just prints a success message.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Test command executed successfully! ✅'))