# Generated by Django 4.2.10 on 2024-02-24 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0004_settings_enable_hostel_limits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='imagekit_private_key',
            field=models.CharField(blank=True, help_text='Used to delete images when a student is deleted.', max_length=100, null=True),
        ),
    ]
