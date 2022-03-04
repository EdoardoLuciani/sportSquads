import os
from unicodedata import category
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportSquads_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from sportSquads.models import UserProfile, Sport, Team
from django.core.files import File

def add_user(username, password, email, first_name, last_name, bio, pfp_path):
    user = User.objects.get_or_create(username=username, password=password, email=email, first_name=first_name, last_name=last_name)[0]
    user.save()

    user_profile = UserProfile.objects.get_or_create(user=user, bio=bio)[0]
    if pfp_path:
        pfp_file = open(pfp_path, mode='rb')
        user_profile.profile_picture = File(pfp_file, name=pfp_file.name)
        user_profile.save()
        pfp_file.close()

    user_profile.save()

    return (user, user_profile)


def populate():

    profile_image_initial_path = './populate_sportSquads_files/profile_images/'
    users_data = [
        {'username': 'kracc bacc', 'password': 'oQSL8ACO', 'email': 'boh@nsa.gov', 'first_name': 'Kracc', 'last_name': 'Bacc', 'bio': 'I am a member of the NSA', 'pfp_path': os.path.join(profile_image_initial_path, 'cat0.png')},
        {'username': 'JohnWilliamson69', 'password': 'Apy3GUIy', 'email': 'lecturer@gmail.com', 'first_name': 'John', 'last_name': 'Williamson', 'bio': 'I am a lecturer', 'pfp_path': os.path.join(profile_image_initial_path, 'cat2.png')},
        {'username': 'Willem_Dafoe', 'password': 'NjB0CA9D', 'email': 'willem.dafoe@microsoft.com', 'first_name': 'Willem', 'last_name': 'Dafoe', 'bio': 'I am an actor', 'pfp_path': ''},
    ]

    for user_data in users_data:
        add_user(**user_data)


if __name__ == '__main__':
    print('Populating sportSquads database...')
    populate()