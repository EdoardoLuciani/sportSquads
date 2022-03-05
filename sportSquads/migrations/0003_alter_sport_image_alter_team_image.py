# Generated by Django 4.0.2 on 2022-03-04 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportSquads', '0002_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='image',
            field=models.ImageField(blank=True, upload_to='sport_images'),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, upload_to='team_images'),
        ),
    ]