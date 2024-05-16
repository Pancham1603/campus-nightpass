from django.core.management.base import BaseCommand
from ...models import NightPass
from ....global_settings.models import Settings as settings
from datetime import date, timedelta, datetime, time
from django.utils import timezone
import pytz

ist_timezone = pytz.timezone('Asia/Kolkata')

def check_defaulters_lib_entry():
    Settings = settings.objects.first()

    # nightpasses = NightPass.objects.filter(date=date.today(), defaulter=True)
    # for nightpass in nightpasses:
    #     nightpass.user.student.violation_flags = NightPass.objects.filter(user=nightpass.user, defaulter=True).count()
    #     nightpass.user.student.defaulter_notification = True
    #     nightpass.user.student.save()

    
    nightpasses = NightPass.objects.filter(date=date.today())
    # nightpasses.update(defaulter=False, defaulter_remarks='')
    for nightpass in nightpasses:
        print(nightpass.user.email)
        defaulter = nightpass.defaulter if nightpass.defaulter else False
        remarks = nightpass.defaulter_remarks if nightpass.defaulter_remarks else ""
        if not nightpass.check_in:
            pass
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
                    if (nightpass.check_in_time.astimezone(ist_timezone).time() > start_default_time):
                        defaulter = True
                        remarks+= f"Late check in at {nightpass.campus_resource.name}" if f"Late check in at {nightpass.campus_resource.name}" not in remarks else remarks
            else:
                if (nightpass.check_in_time.astimezone(ist_timezone).time() > end_default_time):
                    defaulter = True
                    remarks+= f"Late check in at {nightpass.campus_resource.name}" if f"Late check in at {nightpass.campus_resource.name}" not in remarks else remarks
            # if not nightpass.check_out_time:
            #     nightpass.check_out_time = datetime.combine(nightpass.check_in_time.date(), nightpass.campus_resource.closing_time)
            #     nightpass.check_out_time = timezone.make_aware(nightpass.check_out_time, timezone.get_current_timezone())
            #     nightpass.save()
            # if not nightpass.hostel_checkin_time:
            #     defaulter = True
            #     remarks+= "Late check in at hostel"
            # elif (nightpass.hostel_checkin_time - nightpass.check_out_time) > timedelta(minutes=checkin_timer):            
            #     defaulter = True
            #     remarks+= "Late check in at hostel"
            # if (nightpass.check_out_time-nightpass.check_in_time) < timedelta(minutes=10):
            #     defaulter = True
            #     remarks+= f"Stayed for very less time at {nightpass.campus_resource.name}" 

        if defaulter:
            nightpass.defaulter = True
            nightpass.defaulter_remarks = remarks
            nightpass.save()
            nightpass.user.student.violation_flags = NightPass.objects.filter(user=nightpass.user, defaulter=True).count()
            nightpass.user.student.defaulter_notification = True
            nightpass.user.student.save()


class Command(BaseCommand):
    help = 'Check for defaulters'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running your cron job...'))
        check_defaulters_lib_entry()
        self.stdout.write(self.style.SUCCESS('Cron job completed successfully'))

