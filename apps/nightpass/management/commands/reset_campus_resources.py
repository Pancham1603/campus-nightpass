from django.core.management.base import BaseCommand
from ...models import CampusResource

class Command(BaseCommand):
    help = 'Reset all campus resources'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        CampusResource.objects.all().update(slots_booked=0, booking_complete=False, is_booking = False)
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))