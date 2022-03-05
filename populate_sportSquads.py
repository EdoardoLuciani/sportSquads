import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportSquads_project.settings")
django.setup()

from django.contrib.auth.models import User
from sportSquads.models import TeamUserMembership, UserProfile, Sport, Team
from django.core.files import File


# Function to create a new file in the media directory and assign it to a model field
def assign_file_and_save(model_instance, image_field_name, file_path):
    if file_path:
        file = open(file_path, mode="rb")
        setattr(
            model_instance,
            image_field_name,
            File(file, name=os.path.basename(file_path)),
        )
        model_instance.save()
        file.close()
    model_instance.save()


def add_user(username, password, email, first_name, last_name, bio, pfp_path):
    user = User.objects.get_or_create(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )[0]
    user.save()

    user_profile = UserProfile.objects.get_or_create(user=user, bio=bio)[0]
    assign_file_and_save(user_profile, "profile_picture", pfp_path)


def add_sport(name, image_path, description, author, roles):
    sport = Sport.objects.get_or_create(
        name=name, description=description, author=author, roles=roles
    )[0]
    assign_file_and_save(sport, "image", image_path)


def add_team(name, image_path, description, location, sport, manager, members_with_roles):
    available_roles_json = sport.roles
    for (member, role) in members_with_roles:
        available_roles_json[role] = str(int(available_roles_json[role]) - 1)

    team = Team.objects.get_or_create(
        name=name,
        description=description,
        location=location,
        sport=sport,
        manager=manager,
        available_roles=available_roles_json,
    )[0]
    assign_file_and_save(team, "image", image_path)

    for (member, role) in members_with_roles:
        member_with_role_relation = TeamUserMembership(
            user=member, team=team, role=role
        )
        member_with_role_relation.save()


def populate():
    profile_images_initial_path = "./populate_sportSquads_files/profile_images/"
    users_data = [
        {
            "username": "kracc bacc",
            "password": "oQSL8ACO",
            "email": "boh@nsa.gov",
            "first_name": "Kracc",
            "last_name": "Bacc",
            "bio": "I am a member of the NSA",
            "pfp_path": os.path.join(profile_images_initial_path, "cat0.png"),
        },
        {
            "username": "JohnWilliamson69",
            "password": "Apy3GUIy",
            "email": "lecturer@gmail.com",
            "first_name": "John",
            "last_name": "Williamson",
            "bio": "I am a lecturer",
            "pfp_path": os.path.join(profile_images_initial_path, "cat1.png"),
        },
        {
            "username": "Willem_Dafoe",
            "password": "NjB0CA9D",
            "email": "willem.dafoe@microsoft.com",
            "first_name": "Willem",
            "last_name": "Dafoe",
            "bio": "I am an actor",
            "pfp_path": "",
        },
    ]
    for user_data in users_data:
        add_user(**user_data)

    sport_images_initial_path = "./populate_sportSquads_files/sport_images/"
    sports_data = [
        {
            "name": "Football",
            "image_path": os.path.join(sport_images_initial_path, "football.jpg"),
            "description": "Football is a team sport",
            "author": User.objects.get(username="kracc bacc").userprofile,
            "roles": {"manager": "1", "goalkeeper": "1"},
        },
        {
            "name": "Volleyball",
            "image_path": "",
            "description": "Volleyball is a team sport",
            "author": None,
            "roles": {"opposite": "1", "setter": "1"},
        },
    ]
    for sport_data in sports_data:
        add_sport(**sport_data)

    team_images_initial_path = "./populate_sportSquads_files/team_images/"
    teams_data = [
        {
            "name": "YoMama",
            "image_path": os.path.join(team_images_initial_path, "yo_mama.jpg"),
            "description": "We are NOT motivated",
            "location": "somewhere",
            "sport": Sport.objects.get(name="Football"),
            "manager": User.objects.get(username="Willem_Dafoe").userprofile,
            "members_with_roles": [
                (User.objects.get(username="Willem_Dafoe").userprofile, "manager"),
                (User.objects.get(username="JohnWilliamson69").userprofile, "goalkeeper")
            ],
        }
    ]
    for team_data in teams_data:
        add_team(**team_data)


if __name__ == "__main__":
    print("Populating sportSquads database...")
    populate()