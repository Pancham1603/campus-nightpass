# Generated by Django 4.2.7 on 2023-12-11 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='enable_gender_ratio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settings',
            name='female_ratio',
            field=models.FloatField(blank=True, default=0.5, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='male_ratio',
            field=models.FloatField(blank=True, default=0.5, null=True),
        ),
    ]
