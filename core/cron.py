from apps.nightpass.models import CampusResource
from apps.users.models import Student, NightPass
from datetime import timedelta, date

def stop_booking():
    CampusResource.objects.all().update(is_booking=False, booking_complete=True)

def reset_users():
    Student.objects.all().update(is_checked_in=True, last_checkout_time=None, hostel_checkin_time=None, hostel_checkout_time=None)

def reset_nightpass():
    NightPass.objects.all().update(valid=False)

def reset_campus_resources():
    CampusResource.objects.all().update(slots_booked=0, booking_complete=False, is_booking = False)

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
                elif (nightpass.hostel_checkin_time - nightpass.user.student.last_checkout_time) > timedelta(minutes=20):            
                    defaulter = True
                    remarks+= "Entered hostel after 20mins. "
                if (nightpass.check_out_time-nightpass.check_in_time) < timedelta(minutes=20):
                    defaulter = True
                    remarks+= "Time <20min in Location. " 

        if defaulter:
            nightpass.defaulter = True
            nightpass.defaulter_remarks = remarks
            nightpass.save()

                
                

    