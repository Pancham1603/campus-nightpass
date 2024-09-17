# yourapp/management/commands/show_uuids.py

from django.core.management.base import BaseCommand
from apps.users.models import CustomUser

class Command(BaseCommand):
    help = 'Make all users inactive'

    def handle(self, *args, **options):
        CustomUser.objects.all().update(is_active = False)
        self.stdout.write(self.style.SUCCESS('Make all users inactive'))
