# Generated by Django 4.2.7 on 2023-12-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_unique_id_alter_student_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nightpass',
            name='defaulter',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='nightpass',
            name='defaulter_remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]