from django.contrib import admin
from .models import Settings
from ..nightpass.models import CampusResource
from ..users.models import Student, NightPass
from ..users.management.commands.check_defaulters import check_defaulters
from datetime import date, timedelta

from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_sameorigin


class SettingsAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('pk','enable_hostel_limits', 'enable_hostel_timers','enable_gender_ratio','enable_yearwise_limits')

    @button(html_attrs={'style': 'background-color:#88FF88;color:black'})
    def start_booking(self, request):
        def _action(request):
            CampusResource.objects.all().update(is_booking=True, booking_complete=False)
        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed: Start booking", )
    
    @button(html_attrs={'style': 'background-color:#fffd8d;color:black'})
    def stop_booking(self, request):
        def _action(request):
            CampusResource.objects.all().update(is_booking=False, booking_complete=True)
        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed: Stop booking", )
    
    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'})
    def reset_nightpass(self, request):
        def _action(request):
            CampusResource.objects.all().update(slots_booked=0, booking_complete=False, is_booking = False)
            NightPass.objects.filter(date=date.today()-timedelta(days=1)).update(valid=False)
            Student.objects.all().update(is_checked_in=True, last_checkout_time=None, hostel_checkin_time=None, hostel_checkout_time=None, has_booked=False)

        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed: Nightpass reset", )
    
    @button()
    def check_defaulters(self, request):
        def _action(request):
            check_defaulters()
        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed: Check defaulters", )
# Register your models here.
admin.site.register(Settings, SettingsAdmin)