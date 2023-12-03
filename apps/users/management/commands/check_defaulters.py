from django.core.management.base import BaseCommand
from ...models import NightPass, Student
from datetime import date, timedelta

def check_defaulters():
    previous_day_nightpasses = NightPass.objects.filter(date=date.today()-timedelta(days=1))
    for nightpass in previous_day_nightpasses:
        defaulter = False
        remarks = ""
        if not nightpass.check_in:
            defaulter = True
            remarks+= "Did not go to Location. "
        else:
            if not nightpass.check_out:
                defaulter=True
                remarks+= "Left library unethically. "
            else:
                if not nightpass.hostel_checkin_time:
                    defaulter = True
                    remarks+= "Did not enter hostel. "
                elif (nightpass.hostel_checkin_time - nightpass.check_out_time) > timedelta(minutes=20):            
                    defaulter = True
                    remarks+= "Entered hostel after 20mins. "
                if (nightpass.check_out_time-nightpass.check_in_time) < timedelta(minutes=20):
                    defaulter = True
                    remarks+= "Time <20min in Location. " 

        if defaulter:
            nightpass.defaulter = True
            nightpass.defaulter_remarks = remarks
            nightpass.save()
            nightpass.user.student.violation_flags+=1
            nightpass.user.student.save()


class Command(BaseCommand):
    help = 'Check for defaulters'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        check_defaulters()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))

