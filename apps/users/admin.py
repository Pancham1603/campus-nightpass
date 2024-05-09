from django.contrib import admin
from django.apps import apps
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from tablib import Dataset
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
from xlsxwriter import Workbook
from datetime import date, datetime
import io

class YearWiseFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(user__student__year__in=['1',])
        if self.value() == '2':
            return queryset.filter(user__student__year__in=['2',])
        if self.value() == '3':
            return queryset.filter(user__student__year__in=['3',])
        if self.value() == '4':
            return queryset.filter(user__student__year__in=['4',])

class NightPassAdmin(admin.ModelAdmin):
    list_display = ( 'name','user','hostel','date', 'campus_resource','hostel_check_out', 'check_in', 'check_out', 'hostel_check_in', 'defaulter')
    search_fields = ('user__student__name','user__student__registration_number','user__student__email')
    actions = ['export_as_xlsx']
    list_filter = (('date', DateRangeFilter),'campus_resource','user__student__gender','user__student__hostel', YearWiseFilter,'defaulter', 'check_in', 'check_out')
    autocomplete_fields = ('user', 'campus_resource') 
    readonly_fields = ('pass_id')

    def name(self, obj):
        return obj.user.student.name
    
    def hostel(self, obj):
        return obj.user.student.hostel.name

    def hostel_check_out(self, obj):
        return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">') if obj.hostel_checkout_time is not None else format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    
    def hostel_check_in(self, obj):
        return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">') if obj.hostel_checkin_time is not None else format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')

    hostel_check_out.allow_tags = True
    hostel_check_in.allow_tags = True
    hostel_check_out.short_description = 'Hostel Out'
    hostel_check_in.short_description = 'Hostel In'

    def export_as_xlsx(modeladmin, request, queryset):
        headers = ['User', 'Email', 'Hostel', 'Gender','Pass ID', 'Date', 'Campus Resource', 'Check In', 'Check Out', 'Hostel Check Out Time', 'Check In Time', 'Check Out Time' ,'Hostel Check In Time', 'Defaulter', 'Remarks']
        data = []
        for obj in queryset:
            data.append([obj.user.student.name, 
                         obj.user.email ,
                         obj.user.student.hostel.name,
                         obj.user.student.gender,
                         obj.pass_id,
                         obj.date.strftime('%d/%m/%y'),
                         obj.campus_resource.name,
                         obj.check_in, 
                         obj.check_out, 
                         timezone.localtime(obj.hostel_checkout_time).strftime('%H:%M:%S') if obj.hostel_checkout_time is not None else None, 
                         timezone.localtime(obj.check_in_time).strftime('%H:%M:%S') if obj.check_in_time is not None else None, 
                         timezone.localtime(obj.check_out_time).strftime('%H:%M:%S') if obj.check_out_time is not None else None,  
                         timezone.localtime(obj.hostel_checkin_time).strftime('%H:%M:%S') if obj.hostel_checkin_time is not None else None,
                         obj.defaulter,
                         obj.defaulter_remarks])
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
    readonly_fields = ('hostel_checkin_time', 'hostel_checkout_time', 'last_checkout_time',)
    list_filter = ('hostel', YearWiseFilter,'has_booked', 'violation_flags')

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