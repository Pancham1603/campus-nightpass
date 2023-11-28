from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.nightpass.models import CampusResource, Hostel


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True, primary_key=True)
    choices = (('student', 'Student'), ('faculty', 'Faculty'), ('security', 'Security'))
    user_type = models.CharField(max_length=20, choices=choices, default='student')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_related_object(self):
        if self.user_type == 'student':
            return hasattr(self, 'student')
        elif self.user_type == 'faculty':
            return hasattr(self, 'faculty')
        elif self.user_type == 'security':
            return hasattr(self, 'security')
        else:
            return False

    def __str__(self):
        return self.email


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)


    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    registration_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    picture = models.URLField(blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.RESTRICT, related_name='hostel', default=None, blank=True, null=True)
    room_number = models.CharField(max_length=10)
    has_booked = models.BooleanField(default=False)
    is_checked_in = models.BooleanField(default=True)
    hostel_checkout_time = models.DateTimeField(blank=True, null=True)
    hostel_checkin_time = models.DateTimeField(blank=True, null=True)
    last_checkout_time = models.DateTimeField(blank=True, null=True)
    violation_flags = models.IntegerField(default=0)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.registration_number)
    

class Security(models.Model):
    name = models.CharField(max_length=100)
    faculty_incharge = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, null=True, blank=True)
    campus_resource = models.ForeignKey(CampusResource, on_delete=models.CASCADE, null=True, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name
    

class NightPass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pass_id = models.CharField(max_length=20, unique=True, primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    campus_resource = models.ForeignKey(CampusResource, on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)
    hostel_checkin_time = models.DateTimeField(blank=True, null=True)
    hostel_checkout_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.pass_id