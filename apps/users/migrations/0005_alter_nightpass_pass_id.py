# Generated by Django 4.2.7 on 2023-12-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_nightpass_defaulter_nightpass_defaulter_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nightpass',
            name='pass_id',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
