import os
from django.conf import settings
from django.test import TestCase
from sportSquads.models import *
from django.core.files import File

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')
ALL_TEST_FILE_NAMES = [ f for f in os.listdir(TEST_FILES_DIR) ]

# Create the media dir if it doesn't exist
os.makedirs(os.path.join(settings.BASE_DIR, 'media'), exist_ok=True)

def find_and_remove_files(dir, files_to_remove):
    local_directories = []

    for elem_name in os.listdir(dir):
        elem_path = os.path.join(dir, elem_name)

        if elem_name in files_to_remove:
            os.remove(elem_path)
            files_to_remove.remove(elem_name)
        elif os.path.isdir(elem_path):
            local_directories.append(elem_path)
    
    if (len(files_to_remove) > 0):
        for local_dir in local_directories:
            find_and_remove_files(local_dir, files_to_remove)

def reset_media_dir():
    find_and_remove_files(settings.MEDIA_DIR, ALL_TEST_FILE_NAMES.copy())
        

class UserProfileTestCase(TestCase):
    def setUp(self):
        reset_media_dir()

    def tearDown(self):
        reset_media_dir()

    def test_user_profile_creation_with_pfp(self):
        user = User.objects.create(username="testuser", password="testpassword")

        with open(os.path.join(TEST_FILES_DIR, "pfp.jpg"), "rb") as f:
            user_profile = UserProfile.objects.create(user=user, profile_picture=File(f, name="pfp.jpg"), bio="test bio")

        self.assertEqual(user_profile.user.username, "testuser")
        self.assertEqual(str(user_profile), "testuser")
        self.assertEqual(user_profile.user.password, "testpassword")
        self.assertEqual(user_profile.bio, "test bio")

        self.assertEqual(user_profile.profile_picture.url, "/media/profile_images/pfp.jpg")

    def test_user_profile_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        self.assertEqual(user_profile.profile_picture, None)
        self.assertEqual(user_profile.bio, '')


class SportTestCase(TestCase):
    def setUp(self):
        reset_media_dir()

    def tearDown(self):
        reset_media_dir()

    def test_sport_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description", author=user_profile, roles={'test role': 'test role description'})

        self.assertEqual(sport.name, "test sport")
        self.assertEqual(sport.image, None)
        self.assertEqual(sport.description, "test description")
        self.assertEqual(sport.author, user_profile)
        self.assertEqual(sport.roles, {'test role': 'test role description'})
        self.assertEqual(sport.name_slug, "test-sport")

    def test_sport_creation_with_picture(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        with open(os.path.join(TEST_FILES_DIR, "sport.jpg"), "rb") as f:
            sport = Sport.objects.create(name="test sport", image=File(f, name="sport.jpg"), author=user_profile, roles={'test role': 'test role description'})

        self.assertEqual(sport.description, '')
        self.assertEqual(sport.image.url, "/media/sport_images/sport.jpg")


class TeamTestCase(TestCase):
    def setUp(self):
        reset_media_dir()

    def tearDown(self):
        reset_media_dir()

    def test_team_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description", author=user_profile, roles={'test role': 'test role description'})

        team = Team.objects.create(name="test team", sport=sport, description="test description", manager=user_profile, available_roles=sport.roles)

        self.assertEqual(team.name, "test team")
        self.assertEqual(team.sport, sport)
        self.assertEqual(team.description, "test description")
        self.assertEqual(team.manager, user_profile)
        self.assertEqual(team.available_roles, sport.roles)
        self.assertEqual(team.name_slug, "test-team")

    def test_team_creation_with_picture(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description", author=user_profile, roles={'test role': 'test role description'})

        with open(os.path.join(TEST_FILES_DIR, "sport.jpg"), "rb") as f:
            team = Team.objects.create(name="test team", image=File(f, name="sport.jpg"), sport=sport, manager=user_profile, available_roles=sport.roles)

        self.assertEquals(team.image.url, "/media/team_images/sport.jpg")


class TeamUserMembershipTestCase(TestCase):
    def test_team_user_membership_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description", author=user_profile, roles={'test role': 'test role description'})

        team = Team.objects.create(name="test team", sport=sport, description="test description", manager=user_profile, available_roles=sport.roles)

        team_user_membership = TeamUserMembership.objects.create(team=team, user=user_profile, role='test role')

        self.assertEqual(team_user_membership.team, team)
        self.assertEqual(team_user_membership.user, user_profile)
        self.assertEqual(team_user_membership.role, 'test role')