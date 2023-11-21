from django.contrib import admin
from .models import *

# Register your models here.

class CampusResourceAdmin(admin.ModelAdmin):
    list_display = ('name',  'max_capacity', 'slots_booked', 'is_booking', 'is_display', 'booking_complete')
    search_fields = ('name',)

admin.site.register(CampusResource, CampusResourceAdmin)
