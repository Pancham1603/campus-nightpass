# yourapp/management/commands/generate_uuids.py

from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
import uuid

class Command(BaseCommand):
    help = 'Generate UUIDs for existing users in the database'

    def handle(self, *args, **options):
        users_without_uuid = CustomUser.objects.filter(unique_id__isnull=True)
        
        for user in users_without_uuid:
            user.unique_id = uuid.uuid4()
            user.save()
            print(f'[{user.unique_id}] {user.username}')

        self.stdout.write(self.style.SUCCESS('UUIDs generated successfully for existing users.'))
