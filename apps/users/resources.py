from import_export import resources, fields
from .models import Student, CustomUser

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'contact_number', 'registration_number','gender', 'branch', 'date_of_birth', 'father_name', 'mother_name', 'course', 'year', 'parent_contact', 'address', 'picture', 'hostel', 'room_number', 'email')
        import_id_fields = ('registration_number',)

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        user = CustomUser.objects.filter(email=instance.email).first()
        if not user:
            instance.user = CustomUser.objects.create(email=instance.email, user_type='student')
            return super().save_instance(instance, is_create, using_transactions, dry_run)
        else:
            # user.is_active = True
            # user.save()
            try:
                if not user.student:
                    instance.registration_number = int(instance.registration_number)
                    instance.user = user
                    instance.gender = instance.gender.lower()
                    return super().save_instance(instance, is_create, using_transactions, dry_run)
            except:
                    instance.registration_number = int(instance.registration_number)
                    instance.user = user
                    instance.gender = instance.gender.lower()
                    return super().save_instance(instance, is_create, using_transactions, dry_run)


    def get_import_id_fields(self):
        return ('registration_number',)
