from django.core.management.base import BaseCommand
from ...cron import reset_campus_resources

class Command(BaseCommand):
    help = 'Reset campus resources'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        reset_campus_resources()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))