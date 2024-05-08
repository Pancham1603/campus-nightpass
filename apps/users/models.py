from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.nightpass.models import CampusResource, Hostel
from apps.global_settings.models import Settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid
import requests
import os
from dotenv import load_dotenv

load_dotenv()


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
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
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
    registration_number = models.CharField(max_length=20)
    branch = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=(('Male','Male'), ('Female','Female')))
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    picture = models.URLField(blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.RESTRICT, related_name='hostel', default=None, blank=True, null=True)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    has_booked = models.BooleanField(default=False)
    is_checked_in = models.BooleanField(default=True)
    hostel_checkout_time = models.DateTimeField(blank=True, null=True, editable=False)
    hostel_checkin_time = models.DateTimeField(blank=True, null=True, editable=False)
    last_checkout_time = models.DateTimeField(blank=True, null=True, editable=False)
    violation_flags = models.IntegerField(default=0)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    defaulter_notification = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return str(self.registration_number)

@receiver(post_delete, sender=Student)
def delete_image_from_imagekit(sender, instance, **kwargs):
    endpoint = "https://api.imagekit.io/v1/files"
    private_api_key = os.getenv("Imagekit_Private_key")
    if instance.picture:
        params = {
            "name": instance.picture.split('/')[-1],
            "filetype": "image"
        }
        auth = (private_api_key, ":")
        response = requests.get(endpoint, params=params, auth=auth)
        if response.status_code == 200:
            fileId = response.json()[0]['fileId']
            r = requests.delete(f'https://api.imagekit.io/v1/files/{fileId}', auth=auth)


class Security(models.Model):
    name = models.CharField(max_length=100)
    admin_incharge = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, null=True, blank=True)
    campus_resource = models.ForeignKey(CampusResource, on_delete=models.CASCADE, null=True, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Security'
    

class NightPass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pass_id = models.CharField(max_length=20, unique=True, primary_key=True, editable=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(editable=False)
    campus_resource = models.ForeignKey(CampusResource, on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False, editable=False)
    check_out = models.BooleanField(default=False, editable=False)
    check_in_time = models.DateTimeField(blank=True, null=True, editable=False)
    check_out_time = models.DateTimeField(blank=True, null=True, editable=False)
    hostel_checkin_time = models.DateTimeField(blank=True, null=True, editable=False)
    hostel_checkout_time = models.DateTimeField(blank=True, null=True, editable=False)
    valid = models.BooleanField(default=True)
    defaulter = models.BooleanField(default=False, blank=True, null=True)
    defaulter_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pass_id
    
    class Meta:
        verbose_name_plural = 'Night Passes'