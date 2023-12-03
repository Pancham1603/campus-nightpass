from django.core.management.base import BaseCommand
from ...cron import check_defaulters

class Command(BaseCommand):
    help = 'Check for defaulters'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        check_defaulters()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))