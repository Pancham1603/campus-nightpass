from django.db import models

class Settings(models.Model):

    enable_hostel_limits = models.BooleanField(default=False, help_text="Limit the number of students eligible for a particular hostel. Limit can be set from Hostel profile.")
    enable_hostel_timers = models.BooleanField(default=False, help_text="Enabling activates the time limits specified in the Hostel profile. The timers below, however, will not be operational.")
    frontend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)
    backend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)

    last_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)
    valid_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)

    enable_gender_ratio = models.BooleanField(default=False)
    male_ratio = models.FloatField(blank=True, null=True, default=0.5)
    female_ratio = models.FloatField(blank=True, null=True, default=0.5)

    max_violation_count = models.IntegerField(blank=True, null=True, default=3)

    enable_yearwise_limits = models.BooleanField(default=False)
    first_year = models.IntegerField(blank=True, null=True, default=0)
    second_year = models.IntegerField(blank=True, null=True, default=0)
    third_year = models.IntegerField(blank=True, null=True, default=0)
    fourth_year = models.IntegerField(blank=True, null=True, default=0)

    imagekit_private_key = models.CharField(max_length=100, blank=True, null=True, help_text="Used to delete images when a student is deleted.")

    
    class Meta:
        verbose_name_plural = 'Settings'