from apps.nightpass.models import CampusResource
from apps.users.models import Student, NightPass

def reset_nightpass():
    Student.objects.all().update(is_checked_in=True, last_checkout_time=None, hostel_checkin_time=None, hostel_checkout_time=None)
    CampusResource.objects.all().update(slots_booked=0, booking_complete=False)
    