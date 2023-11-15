from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, registration_number, password=None, **extra_fields):
        if not registration_number:
            raise ValueError('The Registration Number field must be set')
        user = self.model(registration_number=registration_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, registration_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(registration_number, password, **extra_fields)
    
class ThaparStaff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    warden = models.ForeignKey(ThaparStaff, on_delete=models.CASCADE)
    caretaker = models.ForeignKey(ThaparStaff, on_delete=models.CASCADE, related_name='caretaker')
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Student(AbstractBaseUser, PermissionsMixin):
    registration_number = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    course = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    qr = models.URLField(blank=True)
    picture = models.URLField(blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.RESTRICT, related_name='hostel', default=None, blank=True, null=True)
    room_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    has_booked = models.BooleanField(default=False)
    is_checked_in = models.BooleanField(default=True)
    hostel_checkout_time = models.DateTimeField(blank=True, null=True)
    hostel_checkin_time = models.DateTimeField(blank=True, null=True)
    last_checkout_time = models.DateTimeField(blank=True, null=True)
    violation_flags = models.IntegerField(default=0)

    USERNAME_FIELD = 'registration_number'

    objects = CustomUserManager()

    def __str__(self):
        return self.registration_number
    

    

