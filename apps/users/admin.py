from django.contrib import admin
from .models import *
# Register your models here.

class NightPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user','date', 'campus_resource', 'check_in', 'check_out')
    search_fields = ('pass_id', 'user__name','user__registration_number', 'campus_resource__name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','registration_number', 'hostel', 'has_booked', 'violation_flags')
    search_fields = ('name','registration_number',)
    autocomplete_fields = ('user',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_type')
    search_fields = ('email',)

admin.site.register(Faculty)
admin.site.register(Student, StudentAdmin)
admin.site.register(Security)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NightPass, NightPassAdmin)

admin.site.site_header = "Thapar NightPass"
admin.site.site_title = "Thapar NightPass"
admin.site.index_title = "Thapar NightPass"