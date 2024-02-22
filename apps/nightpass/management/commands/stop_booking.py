from django.core.management.base import BaseCommand
from ...models import CampusResource

class Command(BaseCommand):
    help = 'Stop booking for all campus resources'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        CampusResource.objects.all().update(is_booking=False, booking_complete=True)
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))