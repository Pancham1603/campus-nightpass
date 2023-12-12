from django.core.management.base import BaseCommand
from ...models import NightPass
from ....global_settings.models import Settings as settings
from datetime import date, timedelta, datetime, time
from django.utils import timezone



def check_defaulters():
    Settings = settings.objects.first()
    previous_day_nightpasses = NightPass.objects.filter(date=date.today()-timedelta(days=1))
    previous_day_nightpasses.update(defaulter=False, defaulter_remarks='')
    for nightpass in previous_day_nightpasses:
        print(nightpass.user.email)
        defaulter = False
        remarks = ""
        if not nightpass.check_in:
            defaulter = True
            remarks+= f"Did not visit {nightpass.campus_resource.name}"
        else:
            # start_default_time = timezone.make_aware(datetime.combine(nightpass.check_in_time.date(), time(20,45)), timezone.get_current_timezone())
            # end_default_time = timezone.make_aware(datetime.combine(nightpass.check_in_time.date(), time(21,00)), timezone.get_current_timezone())
            start_default_time = Settings.valid_entry_without_hostel_checkout
            end_default_time = Settings.last_entry_without_hostel_checkout

            if Settings.enable_hostel_timers:
                checkin_timer = nightpass.user.student.hostel.backend_checkin_timer
            else:
                checkin_timer = Settings.backend_checkin_timer

            if nightpass.hostel_checkout_time:
                if (nightpass.check_in_time - nightpass.hostel_checkout_time) > timedelta(minutes=checkin_timer):
                    if (nightpass.check_in_time.time() > start_default_time):
                        defaulter = True
                        remarks+= f"Late check in at {nightpass.campus_resource.name}"
            else:
                if (nightpass.check_in_time > end_default_time.time()):
                    defaulter = True
                    remarks+= f"Late check in at {nightpass.campus_resource.name}"
            if not nightpass.check_out_time:
                defaulter= True
                remarks+= f"Left {nightpass.campus_resource.name} without checking out."
            else:
                if not nightpass.hostel_checkin_time:
                    defaulter = True
                    remarks+= "Late check in at hostel"
                elif (nightpass.hostel_checkin_time - nightpass.check_out_time) > timedelta(minutes=checkin_timer):            
                    defaulter = True
                    remarks+= "Late check in at hostel"
                if (nightpass.check_out_time-nightpass.check_in_time) < timedelta(minutes=10):
                    defaulter = True
                    remarks+= f"Stayed for very less time at {nightpass.campus_resource.name}" 

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

