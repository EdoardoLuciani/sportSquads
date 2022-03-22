import os
from django.test import TestCase
from sportSquads.models import *
from django.core.files import File

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

ALL_TEST_FILES = [ os.path.join(TEST_FILES_DIR, f) for f in os.listdir(TEST_FILES_DIR) ]

def cleanup():
    for file_name in ALL_TEST_FILES:
        # get filename removing the path
        os.remove(file_name)

class UserProfileTestCase(TestCase):
    def setUp(self):
        cleanup()

    def test_user_profile_creation(self):
        user = User.objects.create(username="testuser", password="testpassword")

        with open(os.path.join(TEST_FILES_DIR, "test_pfp.jpg"), "rb") as f:
            user_profile = UserProfile.objects.create(user=user, profile_picture=File(f, name="test_pfp.jpg"), bio="test bio")

        self.assertEqual(user_profile.user.username, "testuser")
        self.assertEqual(user_profile.profile_picture.url, "/media/profile_images/test_pfp.jpg")
        self.assertEqual(user_profile.bio, "test bio")