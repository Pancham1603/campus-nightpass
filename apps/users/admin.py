from django.contrib import admin
from django.apps import apps
from django.http import HttpResponse
from tablib import Dataset
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
from xlsxwriter import Workbook
from datetime import date, datetime
import io
from django.utils import timezone


class NightPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user','date', 'campus_resource', 'check_in', 'check_out')
    search_fields = ('pass_id', 'user__name','user__registration_number', 'campus_resource__name')
    actions = ['export_as_xlsx']

    def export_as_xlsx(modeladmin, request, queryset):
        headers = ['User', 'Email', 'Hostel', 'Pass ID', 'Date', 'Campus Resource', 'Check In','Check In Time', 'Check Out',  'Check Out Time', 'Hostel Check Out Time' ,'Hostel Check In Time']
        data = []
        for obj in queryset:
            data.append([obj.user.student.name, 
                         obj.user.email ,
                         obj.user.student.hostel.name,
                         obj.pass_id,
                         obj.date.strftime('%d/%m/%y'),
                         obj.campus_resource.name,
                         obj.check_in, 
                         timezone.localtime(obj.check_in_time).strftime('%H:%M:%S') if obj.check_in_time is not None else None, 
                         obj.check_out, 
                         timezone.localtime(obj.check_out_time).strftime('%H:%M:%S') if obj.check_out_time is not None else None,  
                         timezone.localtime(obj.hostel_checkout_time).strftime('%H:%M:%S') if obj.hostel_checkout_time is not None else None, 
                         timezone.localtime(obj.hostel_checkin_time).strftime('%H:%M:%S') if obj.hostel_checkin_time is not None else None,])
        output = io.BytesIO()
        wb = Workbook(output, {'in_memory': True, 'remove_timezone':True})
        ws = wb.add_worksheet()

        for col_num, header in enumerate(headers):
            ws.write(0, col_num, header)

        for row_num, obj in enumerate(data, start=1):
            for col_num, cell_value in enumerate(obj):
                    ws.write(row_num, col_num, cell_value)
        wb.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="nightpass_{date.today()}.xlsx"'        
        output.close()

        return response
    export_as_xlsx.short_description = "Export Selected as XLSX"

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('name','registration_number', 'hostel', 'has_booked', 'violation_flags')
    search_fields = ('name','registration_number',)
    autocomplete_fields = ('user',)
    resource_class = StudentResource

class SecurityAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_incharge', 'user')
    search_fields = ('name', 'admin_incharge', 'user')
    autocomplete_fields = ('user',)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'designation', 'department', "staff_id")
    search_fields = ('name', 'user', 'designation', 'department', "staff_id")
    autocomplete_fields = ('user',)

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