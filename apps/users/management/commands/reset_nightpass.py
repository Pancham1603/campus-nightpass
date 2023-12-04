from django.core.management.base import BaseCommand
from ...models import NightPass
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Reset all nightpasses'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        NightPass.objects.filter(data=date.today()-timedelta(days=1)).update(valid=False)
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))