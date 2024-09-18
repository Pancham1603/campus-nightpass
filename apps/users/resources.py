from import_export import resources, fields
from .models import Student, CustomUser
import hashlib

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'contact_number', 'registration_number', 'gender', 'branch', 'date_of_birth', 
                  'father_name', 'mother_name', 'course', 'year', 'parent_contact', 'address', 'picture', 
                  'hostel', 'room_number', 'email')
        import_id_fields = ('registration_number',)  # Keep only fields that exist

    def before_import(self, dataset, **kwargs):
        # Ensure 'id' is calculated but not added as a field
        dataset.headers.append("id")
        super().before_import(dataset, **kwargs)

    def before_import_row(self, row, **kwargs):
        # Generate id from registration_number for internal processing
        row["id"] = hashlib.sha256(row["registration_number"].encode()).hexdigest()

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
        
        # Finally, save the instance
        return super().save_instance(instance, is_create, using_transactions, dry_run)
