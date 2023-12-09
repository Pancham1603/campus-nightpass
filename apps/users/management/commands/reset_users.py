from django.core.management.base import BaseCommand
from ...models import Student

class Command(BaseCommand):
    help = 'Reset all users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        Student.objects.all().update(is_checked_in=True, last_checkout_time=None, hostel_checkin_time=None, hostel_checkout_time=None, has_booked=False)
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))