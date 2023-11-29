from import_export import resources, fields
from .models import Student, CustomUser

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'contact_number', 'registration_number', 'branch', 'date_of_birth', 'father_name', 'mother_name', 'course', 'semester', 'parent_contact', 'address', 'picture', 'hostel', 'room_number', 'email')

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        user = CustomUser.objects.filter(email=instance.email).first()
        if not user:
            instance.user = CustomUser.objects.create(email=instance.email, user_type='student')
            return super().save_instance(instance, is_create, using_transactions, dry_run)
        else:
            if not user.student:
                instance.user = user
                return super().save_instance(instance, is_create, using_transactions, dry_run)

    def get_import_id_fields(self):
        return ['registration_number']
