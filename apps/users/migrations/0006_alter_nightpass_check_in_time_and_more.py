# Generated by Django 4.2.7 on 2023-12-03 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_nightpass_pass_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nightpass',
            name='check_in_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='nightpass',
            name='check_out_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='nightpass',
            name='hostel_checkin_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='nightpass',
            name='hostel_checkout_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='hostel_checkin_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='hostel_checkout_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_checkout_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]