# yourapp/management/commands/show_uuids.py

from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
import uuid

class Command(BaseCommand):
    help = 'Print UUIDs for existing users in the database'

    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            print(user.unique_id)

        self.stdout.write(self.style.SUCCESS('Printed existing UUIDs for users in the database.'))
