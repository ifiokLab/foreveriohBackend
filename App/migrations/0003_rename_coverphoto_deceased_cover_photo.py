# Generated by Django 4.1.6 on 2023-12-05 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_deceased'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deceased',
            old_name='coverPhoto',
            new_name='cover_photo',
        ),
    ]