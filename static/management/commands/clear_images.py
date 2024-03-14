from django.core.management.base import BaseCommand
from ...models import Student

class Command(BaseCommand):
    help = 'Clear all images'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your job...'))
        Student.objects.all().update(picture='')
        self.stdout.write(self.style.SUCCESS('Job completed successfully'))