# Generated by Django 4.1.6 on 2023-12-07 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_deceased_relationship_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deceased',
            name='cover_photo',
            field=models.ImageField(default='cover-photo/profile.jpg', upload_to='cover-photo/'),
        ),
    ]
