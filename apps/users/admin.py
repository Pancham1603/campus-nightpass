from django.contrib import admin
from django.apps import apps
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import StudentResource


class NightPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user','date', 'campus_resource', 'check_in', 'check_out')
    search_fields = ('pass_id', 'user__name','user__registration_number', 'campus_resource__name')

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('name','registration_number', 'hostel', 'has_booked', 'violation_flags')
    search_fields = ('name','registration_number',)
    autocomplete_fields = ('user',)
    resource_class = StudentResource

class SecurityAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_incharge', 'user')
    search_fields = ('name', 'admin_incharge', 'user')

class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'designation', 'department', "staff_id")
    search_fields = ('name', 'user', 'designation', 'department', "staff_id")

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_type')
    search_fields = ('email',)

    def is_admin(self):
        if self.user_type == 'admin':
            return True
    def is_student(self):
        if self.user_type == 'student':
            return True
    def is_security(self):
        if self.user_type == 'security':
            return True
    def get_user_type(self):
        return apps.get_model('users', self.user_type)

admin.site.register(Admin, AdminAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NightPass, NightPassAdmin)

admin.site.site_header = "Thapar NightPass"
admin.site.site_title = "Thapar NightPass"
admin.site.index_title = "Thapar NightPass"