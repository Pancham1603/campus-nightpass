from django.db import models

class Settings(models.Model):

    enable_hostel_timers = models.BooleanField(default=False)
    frontend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)
    backend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)

    last_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)
    valid_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)

    enable_gender_ratio = models.BooleanField(default=False)
    male_ratio = models.FloatField(blank=True, null=True, default=0.5)
    female_ratio = models.FloatField(blank=True, null=True, default=0.5)

    max_violation_count = models.IntegerField(blank=True, null=True, default=3)
    
    class Meta:
        verbose_name_plural = 'Settings'