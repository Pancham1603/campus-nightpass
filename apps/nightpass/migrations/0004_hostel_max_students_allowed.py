# Generated by Django 4.2.7 on 2024-02-03 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nightpass', '0003_hostel_backend_checkin_timer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='max_students_allowed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
