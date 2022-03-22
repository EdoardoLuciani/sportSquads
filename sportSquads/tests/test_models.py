import os
from django.conf import settings
from django.test import TestCase
from sportSquads.models import *
from django.core.files import File

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

ALL_TEST_FILE_NAMES = [ f for f in os.listdir(TEST_FILES_DIR) ]

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

def cleanup():
    find_and_remove_files(settings.MEDIA_DIR, ALL_TEST_FILE_NAMES.copy())
        

class UserProfileTestCase(TestCase):
    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()

    def test_user_profile_creation_with_pfp(self):
        user = User.objects.create(username="testuser", password="testpassword")

        with open(os.path.join(TEST_FILES_DIR, "test_pfp.jpg"), "rb") as f:
            user_profile = UserProfile.objects.create(user=user, profile_picture=File(f, name="test_pfp.jpg"), bio="test bio")

        self.assertEqual(user_profile.user.username, "testuser")
        self.assertEqual(user_profile.user.password, "testpassword")
        self.assertEqual(user_profile.profile_picture.url, "/media/profile_images/test_pfp.jpg")
        self.assertEqual(user_profile.bio, "test bio")

    def test_user_profile_creation_without_pfp(self):
        user = User.objects.create(username="testuser", password="testpassword")
        user_profile = UserProfile.objects.create(user=user, profile_picture=None)

        self.assertEqual(user_profile.user.username, "testuser")
        self.assertEqual(user_profile.profile_picture, None)
        self.assertEqual(user_profile.bio, '')