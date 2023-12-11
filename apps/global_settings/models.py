from django.db import models

class Settings(models.Model):

    enable_hostel_timers = models.BooleanField(default=False)
    frontend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)
    backend_checkin_timer = models.IntegerField(blank=True, null=True, default=0)

    last_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)
    valid_entry_without_hostel_checkout = models.TimeField(blank=True, null=True)

    
    def __str__(self):
        return self.name