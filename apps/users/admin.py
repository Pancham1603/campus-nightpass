from django.contrib import admin
from django.apps import apps
from django import forms
from .models import *
from .forms import StudentUploadForm
import Pandas as pd
# Register your models here.

class NightPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user','date', 'campus_resource', 'check_in', 'check_out')
    search_fields = ('pass_id', 'user__name','user__registration_number', 'campus_resource__name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','registration_number', 'hostel', 'has_booked', 'violation_flags')
    search_fields = ('name','registration_number',)
    autocomplete_fields = ('user',)
    actions = ['import_student_data',]

    def import_student_data(self, request):
        form = StudentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                data = pd.read_excel(file)

                for index,row in data.iterrows():
                    user = CustomUser(
                        email = row['email'],
                        user_type = 'student',
                    )
                    user.save()

                    student = Student(
                        name = row['name'],
                        contact_number = row['contact_number'],
                        registration_number = row['registration_number'],
                        branch = row['branch'],
                        date_of_birth = row['date_of_birth'],
                        father_name = row['father_name'],
                        mother_name = row['mother_name'],
                        course = row['course'],
                        semester = row['semester'],
                        parent_contact = row['parent_contact'],
                        address = row['address'],
                        picture = row['picture'],
                        hostel = Hostel.objects.get(name=row['hostel']),
                        room_number = row['room_number'],
                        user = user
                    )
                    student.save()
                self.message_user(request, f'Successfully imported data from {file.name}.')
            except Exception as e:
                self.message_user(request, f'Error importing data: {str(e)}', level='error')
        else:
            self.message_user(request, 'Invalid form submission. Please check the file.', level='error')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_type')
    search_fields = ('email',)

    def is_faculty(self):
        if self.user_type == 'faculty':
            return True
    def is_student(self):
        if self.user_type == 'student':
            return True
    def is_security(self):
        if self.user_type == 'security':
            return True
    def get_user_type(self):
        return apps.get_model('users', self.user_type)

admin.site.register(Faculty)
admin.site.register(Student, StudentAdmin)
admin.site.register(Security)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NightPass, NightPassAdmin)

admin.site.site_header = "Thapar NightPass"
admin.site.site_title = "Thapar NightPass"
admin.site.index_title = "Thapar NightPass"