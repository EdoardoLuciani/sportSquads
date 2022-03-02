from django.db import models
from django.template.defaultfilters import slugify


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    profile_picture = models.ImageField(blank=True)
    bio = models.TextField()
    username_slug = models.SlugField(unique=True)   # username appears in some urls so slugging it

    def save(self, *args, **kwargs):
        self.username_slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Sport(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.JSONField()
    name_slug = models.SlugField(unique=True)   # sport name appears in some urls so slugging it

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Sport, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(blank=True)
    description = models.TextField()
    location = models.CharField(128)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    members_with_roles = models.ManyToManyField(User, through="TeamUserMembership")
    available_roles = models.JSONField()
    name_slug = models.SlugField(unique=True)   # team name appears in some urls so slugging it

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


# this class is so that we can have the (member, role) in the Team class
# could add more fields here such as date joined, reason for joining etc.
class TeamUserMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    role = models.CharField(max_length=64)


