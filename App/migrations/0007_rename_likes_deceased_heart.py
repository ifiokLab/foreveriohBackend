# Generated by Django 4.1.6 on 2023-12-14 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_tribute_deceased_likes_deceased_share_tributereply_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deceased',
            old_name='likes',
            new_name='heart',
        ),
    ]