from django.core.management.base import BaseCommand
from ...models import NightPass

class Command(BaseCommand):
    help = 'Reset all nightpasses'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        NightPass.objects.all().update(valid=False)
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))