import os
from django.conf import settings
from django.test import TestCase
from sportSquads.models import *
from django.core.files import File
from sportSquads.forms import *

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')


class SportFormTests(TestCase):

    def test_form_valid_no_image(self):
        form = SportForm(data={'name': 'New Sport', 'description': 'A team desc', 'role_0': 'yes a role'})

        self.assertTrue(form.is_valid())

    def test_form_valid_with_image(self):
        with open(os.path.join(TEST_FILES_DIR, "sport.jpg"), "rb") as f:
            profile_picture = File(f, name="sport.jpg")

        form = SportForm(data={'name': 'New Sport', 'description': 'A team desc', 'image': profile_picture})

        self.assertTrue(form.is_valid())

    def test_null_form_invalid(self):
        form = SportForm(data={})
        self.assertFalse(form.is_valid())


class TeamFormTests(TestCase):

    def test_form_valid_no_image(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description",
                                     author=user_profile, roles={'test role': 3})

        form = TeamForm(manager=user_profile, sport=sport, data={'name': 'test', 'description': 'test description',
                                                                 'location': 'test location', 'initial_role': '0'})
        self.assertTrue(form.is_valid())

    def test_form_valid_with_image(self):
        with open(os.path.join(TEST_FILES_DIR, "sport.jpg"), "rb") as f:
            team_image = File(f, name="sport.jpg")

        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description",
                                     author=user_profile, roles={'test role': 3})

        form = TeamForm(manager=user_profile, sport=sport, data={'name': 'test', 'description': 'test description',
                                                                 'location': 'test location', 'initial_role': '0',
                                                                 'image': team_image})
        self.assertTrue(form.is_valid())

    def test_null_form_invalid(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description",
                                     author=user_profile, roles={'test role': 3})
        form = TeamForm(manager=user_profile, sport=sport, data={'initial_role': '0'})

        self.assertFalse(form.is_valid())


class JoinTeamTests(TestCase):

    def test_role_picked_valid(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        sport = Sport.objects.create(name="test sport", image=None, description="test description",
                                     author=user_profile, roles={'test role': 3})

        team = Team.objects.create(name="test team", sport=sport, manager=user_profile,
                                   available_roles=sport.roles)

        form = JoinTeamForm(team=team, user=user, data={'role': '0'})

        self.assertTrue(form.is_valid())
