from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.nightpass.models import CampusResource, Hostel
import uuid


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
        extra_fields.setdefault('user_type', 'admin')


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    choices = (('student', 'Student'), ('admin', 'Admin'), ('security', 'Security'))
    user_type = models.CharField(max_length=20, choices=choices, default='student')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_related_object(self):
        if self.user_type == 'student':
            return hasattr(self, 'student')
        elif self.user_type == 'admin':
            return hasattr(self, 'admin')
        elif self.user_type == 'security':
            return hasattr(self, 'security')
        else:
            return False

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.user_type == 'security':
            self.is_staff = True
        elif self.user_type == 'admin':
            self.is_superuser = True
        super().save(*args, **kwargs)

class Admin(models.Model):
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
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    semester = models.CharField(max_length=10, null=True, blank=True)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    picture = models.URLField(blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.RESTRICT, related_name='hostel', default=None, blank=True, null=True)
    room_number = models.CharField(max_length=10, null=True, blank=True)
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
    admin_incharge = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, null=True, blank=True)
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
    valid = models.BooleanField(default=True)
    defaulter = models.BooleanField(default=False, blank=True, null=True)
    defaulter_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pass_id