from import_export import resources
from .models import Student, CustomUser
from ..nightpass.models import Hostel

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = (
            'name', 'contact_number', 'registration_number', 'gender', 'branch', 
            'date_of_birth', 'father_name', 'mother_name', 'course', 'year', 
            'parent_contact', 'address', 'picture', 'hostel', 'room_number', 'email'
        )

    def before_import_row(self, row, **kwargs):
        # Ensure registration_number is an integer
        row['registration_number'] = int(row.get('registration_number', 0))
        
        # Set gender to lowercase
        row['gender'] = row.get('gender', '').lower()

        # Handle CustomUser creation or retrieval
        email = row.get('email')
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                # Create a new CustomUser if it doesn't exist
                user = CustomUser.objects.create(email=email, user_type='student')
            row['user'] = user.id  # Associate CustomUser with the Student object
        else:
            raise ValueError("Email is required for importing students.")

        # Handle Student creation or retrieval
        registration_number = row.get('registration_number')
        student = Student.objects.filter(registration_number=registration_number).first()
        if not student:
            # Create the student object if it doesn't exist
            Student.objects.create(
                name=row.get('name'),
                contact_number=row.get('contact_number'),
                registration_number=row.get('registration_number'),
                gender=row.get('gender').title(),
                branch=row.get('branch'),
                father_name=row.get('father_name'),
                mother_name=row.get('mother_name'),
                course=row.get('course'),
                year=row.get('year'),
                parent_contact=row.get('parent_contact'),
                address=row.get('address'),
                picture=row.get('picture'),
                hostel= Hostel.objects.filter(name=row.get('hostel')).first() ,
                room_number=row.get('room_number'),
                email=row.get('email'),
                user=user  # Associate with the newly created CustomUser
            )
        else:
            # Associate the existing student with the found user
            student.user = user
            student.gender = student.gender.title()
            student.save()

    def get_import_id_fields(self):
        return ['registration_number']
