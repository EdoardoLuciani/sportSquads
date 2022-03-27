# Generated by Django 4.0.2 on 2022-03-27 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='sport_images')),
                ('description', models.TextField(blank=True)),
                ('roles', models.JSONField()),
                ('name_slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='team_images')),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(max_length=128)),
                ('available_roles', models.JSONField()),
                ('name_slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamUserMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=64)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportSquads.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportSquads.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='sportSquads.userprofile'),
        ),
        migrations.AddField(
            model_name='team',
            name='members_with_roles',
            field=models.ManyToManyField(related_name='members_with_roles', through='sportSquads.TeamUserMembership', to='sportSquads.UserProfile'),
        ),
        migrations.AddField(
            model_name='team',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sportSquads.sport'),
        ),
        migrations.AddField(
            model_name='sport',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sportSquads.userprofile'),
        ),
    ]
