# Generated by Django 4.2.7 on 2023-11-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nightpass',
            name='valid',
            field=models.BooleanField(default=True),
        ),
    ]
