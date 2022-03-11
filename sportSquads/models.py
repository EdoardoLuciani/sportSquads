import django.contrib.auth.models
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Sport(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='sport_images', blank=True)
    description = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    positions = models.IntegerField(default=5)
    name_slug = models.SlugField(unique=True)   # sport name appears in some urls so slugging it

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Sport, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='team_images', blank=True)
    description = models.TextField()
    location = models.CharField(max_length=128)
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT)

    # related name is so that django can distinguish between the two FKs
    manager = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="manager")
    members_with_roles = models.ManyToManyField(UserProfile, through="TeamUserMembership", related_name="member_with_roles")

    positions_available = models.IntegerField(default=5)
    name_slug = models.SlugField(unique=True)   # team name appears in some urls so slugging it

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


# this class is so that we can have the (member, role) in the Team class
# could add more fields here such as date joined, reason for joining etc.
class TeamUserMembership(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    role = models.CharField(max_length=64)


