from import_export import resources, fields
from .models import Student, CustomUser
import hashlib

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'contact_number', 'registration_number', 'gender', 'branch', 'date_of_birth', 
                  'father_name', 'mother_name', 'course', 'year', 'parent_contact', 'address', 'picture', 
                  'hostel', 'room_number', 'email')
        import_id_fields = ('registration_number',)  # Use 'registration_number' as the unique ID

    def before_import_row(self, row, **kwargs):
        # Generate id internally from registration_number
        internal_id = hashlib.sha256(row["registration_number"].encode()).hexdigest()
        row["internal_id"] = internal_id  # This will not interfere with the dataset headers

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        user = CustomUser.objects.filter(email=instance.email).first()
        if not user:
            instance.user = CustomUser.objects.create(email=instance.email, user_type='student')
        else:
            user.is_active = True
            user.save()
            if not hasattr(user, 'student'):  # Check if user already has a student instance
                instance.registration_number = int(instance.registration_number)
                instance.user = user
                instance.gender = instance.gender.lower()
        
        # Save the instance
        return super().save_instance(instance, is_create, using_transactions, dry_run)
