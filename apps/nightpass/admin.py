from django.contrib import admin
from .models import *

# Register your models here.

class CampusResourceAdmin(admin.ModelAdmin):
    list_display = ('name',  'max_capacity', 'slots_booked', 'is_booking', 'is_display', 'booking_complete')
    search_fields = ('name',)

class NightPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user','date', 'campus_resource', 'check_in', 'check_out')
    search_fields = ('pass_id', 'user__name','user__registration_number', 'campus_resource__name')


admin.site.register(CampusResource, CampusResourceAdmin)
admin.site.register(NightPass, NightPassAdmin)
