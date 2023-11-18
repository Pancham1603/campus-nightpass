from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from apps.users.models import Student 

class CampusResource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.URLField(blank=True)
    max_capacity = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booking = models.BooleanField(default=False)
    is_display = models.BooleanField(default=False)
    booking_complete = models.BooleanField(default=False)
    slots_booked = models.IntegerField(default=0)
    type = models.CharField(max_length=100, choices=[('hostel', 'Hostel'), ('location', 'Location'), ('gate', 'Gate')], null=True, blank=True)


    def __str__(self):
        return self.name

class NightPass(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    pass_id = models.CharField(max_length=20, unique=True, primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    campus_resource = models.ForeignKey(CampusResource, on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.pass_id

