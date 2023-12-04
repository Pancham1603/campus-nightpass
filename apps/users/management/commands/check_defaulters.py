from django.core.management.base import BaseCommand
from ...models import NightPass, Student
from datetime import date, timedelta, datetime, time
from django.utils import timezone


def check_defaulters():
    previous_day_nightpasses = NightPass.objects.filter(date=date.today()-timedelta(days=1))
    for nightpass in previous_day_nightpasses:
        print(nightpass.user.email)
        defaulter = False
        remarks = ""
        if not nightpass.check_in:
            defaulter = True
            remarks+= "Did not go to Location. "
        else:
            start_default_time = timezone.make_aware(datetime.combine(nightpass.check_in_time.date(), time(20,45)), timezone.get_current_timezone())
            end_default_time = timezone.make_aware(datetime.combine(nightpass.check_in_time.date(), time(21,00)), timezone.get_current_timezone())
            if nightpass.hostel_checkout_time:
                if (nightpass.check_in_time - nightpass.hostel_checkout_time) > timedelta(minutes=30):
                    if (nightpass.check_in_time > start_default_time):
                        defaulter = True
                        remarks+= "Entered library after 30mins. "
            else:
                if (nightpass.check_in_time > end_default_time):
                    defaulter = True
                    remarks+= "Entered library after 30mins. "
            if not nightpass.check_out_time:
                defaulter=True
                remarks+= "Left library unethically. "
            else:
                if not nightpass.hostel_checkin_time:
                    defaulter = True
                    remarks+= "Did not enter hostel. "
                elif (nightpass.hostel_checkin_time - nightpass.check_out_time) > timedelta(minutes=30):            
                    defaulter = True
                    remarks+= "Entered hostel after 30mins. "
                if (nightpass.check_out_time-nightpass.check_in_time) < timedelta(minutes=10):
                    defaulter = True
                    remarks+= "Time <10min in Location. " 

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

