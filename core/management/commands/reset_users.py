from django.core.management.base import BaseCommand
from ...cron import reset_users

class Command(BaseCommand):
    help = 'Reset users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        reset_users()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))