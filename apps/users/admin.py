from django.contrib import admin
from .models import *
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name', 'email')
    search_fields = ('registration_number', 'name', 'email')

admin.site.register(Student, StudentAdmin)
admin.site.register(ThaparStaff)
admin.site.register(Hostel)

admin.site.site_header = "Thapar NightPass"
admin.site.site_title = "Thapar NightPass"
admin.site.index_title = "Thapar NightPass"