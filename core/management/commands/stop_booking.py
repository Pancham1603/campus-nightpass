from django.core.management.base import BaseCommand
from ...cron import stop_booking

class Command(BaseCommand):
    help = 'Stop booking for all campus resources'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        stop_booking()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))