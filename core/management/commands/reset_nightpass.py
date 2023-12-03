from django.core.management.base import BaseCommand
from ...cron import reset_nightpass

class Command(BaseCommand):
    help = 'Reset nightpass'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        reset_nightpass()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))