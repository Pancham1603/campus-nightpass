from django.core.management.base import BaseCommand
from ...models import NightPass, Student
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Mark booked users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        today_passes = NightPass.objects.filter(date=date.today())
        today_passes.update(valid=True)
        for night_pass in today_passes:
            night_pass.user.student.has_booked = True
            night_pass.user.student.save()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))