from doctest import testfile
import json
from multiprocessing import dummy
from django.test import TestCase
from sportSquads.models import *
from django.urls import reverse

def create_footballs(user=None, count=300):
    sport_data = {
        "name": "Football",
        "description": "Football is a team sport",
        "roles": {"manager": "1", "goalkeeper": "5"},
        "author": user
    }
    for i in range(0, count):
        sport_to_add = sport_data.copy()
        sport_to_add["name"] = sport_to_add["name"] + str(i)
        Sport.objects.create(**sport_to_add)

def create_football_teams(sport, manager, member_and_role, count=300):
    available_roles_json = sport.roles.copy()

    for _, role in member_and_role:
        available_roles_json[role] = str(int(available_roles_json[role]) - 1)

    team_data = {
        "name": "FootballTeam",
        "description": "boi",
        "location": "somewhere",
        "sport": sport,
        "manager": manager,
        "available_roles": available_roles_json
    }

    for i in range(0, count):
        team_to_add = team_data.copy()
        team_to_add["name"] = team_to_add["name"] + str(i)
        team = Team.objects.create(**team_to_add)

        for member, role in member_and_role:
            TeamUserMembership.objects.create(user=member, team=team, role=role)

def create_users(count=10):
    for i in range(0, count):
        user = User.objects.create_user(username="test" + str(i), password="test")
        UserProfile.objects.create(user=user)

def create_dummy_users(count=10):
    for i in range(0, count):
        user = User.objects.create_user(username="dummy" + str(i), password="dummy")
        user_info = UserProfile.objects.create(bio="blah", user=user)

def create_full_user_and_login(client):
    user = User.objects.create_user(username="test", password="test")
    client.login(username="test", password="test")
    user_info = UserProfile.objects.create(bio="blah", user=user)
    return user_info


class HomeViewTests(TestCase):
    def test_home_view_no_sports(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no sports.")

    def test_home_view(self):
        create_footballs()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['sports'], Sport.objects.filter(name__icontains="Football")[:10], ordered=False)

    def test_home_view_filter(self):
        create_footballs()
        response = self.client.post(reverse("home"), data={"search_text": "ball69"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['sports'], Sport.objects.filter(name="Football69"), ordered=False)


class HomeGet10MoreSportsTests(TestCase):
    def test_home_get_10_more_sports(self):
        create_footballs()
        response = self.client.get(reverse("home_get_sports", args=(3,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["sports"]), 10)
        for i,data in enumerate(response_data["sports"]):
            self.assertEqual(data["name"], "Football" + str(i+3))

    def test_home_get_10_more_sports_end(self):
        create_footballs()
        response = self.client.get(reverse("home_get_sports", args=(10000,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["sports"]), 0)

    def test_home_get_10_more_sports_near_end(self):
        create_footballs()
        response = self.client.get(reverse("home_get_sports", args=(297,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["sports"]), 3)
        for i,data in enumerate(response_data["sports"]):
            self.assertEqual(data["name"], "Football" + str(i+297))


class AccountInformationTests(TestCase):
    def test_account_information_no_user(self):
        response = self.client.get(reverse("account_information"))
        self.assertEqual(response.status_code, 302)

    def test_account_information(self):
        user = create_full_user_and_login(self.client)

        response = self.client.get(reverse("account_information"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], user.user)

    def test_account_information_with_sports(self):
        user = create_full_user_and_login(self.client)
        create_footballs(user=user, count=10)

        response = self.client.get(reverse("account_information"))
        self.assertEqual(response.status_code, 200)

        for i in range(0, 10):
            self.assertContains(response, "Football" + str(i))


class ShowSportTests(TestCase):
    def test_show_sport_not_exist(self):
        response = self.client.get(reverse("show_sport", args=(0,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sport does not exist.")
    
    def test_show_sport(self):
        create_footballs(count=1)
        response = self.client.get(reverse("show_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Football0")

    def test_show_sport_with_teams(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=10)

        response = self.client.get(reverse("show_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        for i in range(0, 10):
            self.assertContains(response, "FootballTeam" + str(i))


class ShowSportGet10MoreTeamsTests(TestCase):
    def test_show_sport_get_10_more_teams(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=20)

        response = self.client.get(reverse("sport_get_teams", args=(Sport.objects.get(name="Football0").name_slug, 3,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["teams"]), 10)
        for i,data in enumerate(response_data["teams"]):
            self.assertEqual(data["name"], "FootballTeam" + str(i+3))

    def test_show_sport_get_10_more_teams_end(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=10)

        response = self.client.get(reverse("sport_get_teams", args=(Sport.objects.get(name="Football0").name_slug, 10000,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["teams"]), 0)

    def test_show_sport_get_10_more_teams_near_end(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=10)


class SearchTeamsTests(TestCase):
    def test_name_query(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=30)

        response = self.client.post(reverse("search_teams"), data={'search_text': 'FootballTeam0', 'filters_team_name': ['1']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FootballTeam0")
        self.assertNotContains(response, "FootballTeam1")

    def test_sport_query(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=30)

        response = self.client.post(reverse("search_teams"), data={'search_text': 'Football', 'filters_team_name': ['4']})
        self.assertEqual(response.status_code, 200)
        for i in range(0, 30):
            self.assertContains(response, "FootballTeam" + str(i))


class ShowTeamTests(TestCase):    
    def test_show_team(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=1)

        response = self.client.get(reverse("show_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FootballTeam0")

    def test_show_team_with_players(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_dummy_users(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager"), (User.objects.get(username="dummy0").userprofile, "goalkeeper")], count=1)

        response = self.client.get(reverse("show_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "test")
        self.assertContains(response, "dummy0")


class JoinTeamTests(TestCase):
    def test_join_team(self):
        create_footballs(count=1)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager")], count=1)

        user = create_full_user_and_login(self.client)

        response = self.client.post(reverse("join_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)), data={'role': '0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are already a member of this team.")

    def test_join_team_already_joined(self):
        create_footballs(count=1)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager")], count=1)

        user = create_full_user_and_login(self.client)

        response = self.client.post(reverse("join_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)), data={'role': '0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are already a member of this team.")

        response = self.client.get(reverse("join_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are already a member of this team.")

    def test_join_team_already_full(self):
        create_footballs(count=1)
        create_dummy_users(count=6)

        dummy_users = [(User.objects.get(username="dummy0").userprofile, "manager")]
        for i in range(1, 6):
            dummy_users.append((User.objects.get(username="dummy" + str(i)).userprofile, "goalkeeper")) 
        create_football_teams(Sport.objects.get(name="Football0"), dummy_users[0][0], dummy_users, count=1)

        user = create_full_user_and_login(self.client)
        response = self.client.get(reverse("join_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No spaces left in the team.")


class SignUpTests(TestCase):
    def test_signup_get(self):
        response = self.client.get(reverse("sign_up"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a new account")

    def test_signup_post(self):
        response = self.client.post(reverse("sign_up"), data={"username": "test", "email": "goo@gmail.com", "password1": "Eu%tc2DM7Mt_h2%F", "password2": "Eu%tc2DM7Mt_h2%F"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], User.objects.get(username="test"))


class LoginTests(TestCase):
    def test_login_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_login_get(self):
        user = create_full_user_and_login(self.client)
        self.client.logout()

        response = self.client.post(reverse("login"), data={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))


class LogoutTests(TestCase):
    def test_logout(self):
        user = create_full_user_and_login(self.client)

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))


class ContactUsTests(TestCase):
    def test_contactus(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")


class AddNewSportTests(TestCase):
    def test_add_new_sport_not_logged(self):
        response = self.client.get(reverse("add_new_sport"))
        self.assertEqual(response.status_code, 302)

    def test_add_new_sport_get(self):
        user = create_full_user_and_login(self.client)
        response = self.client.get(reverse("add_new_sport"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a New Sport")

    def test_add_new_sport_post(self):
        user = create_full_user_and_login(self.client)

        response = self.client.post(reverse("add_new_sport"), data={'name': 'New Sport', 'description': 'A team desc',
         'role_0': 'yes a role', 'role_0_count': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("show_sport", args=("new-sport",)))
        self.assertTrue(Sport.objects.filter(name="New Sport").exists())


class AddNewTeamTests(TestCase):
    def test_add_new_team_not_logged(self):
        create_footballs(count=1)
        response = self.client.get(reverse("add_new_team", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 302)

    def test_add_new_team_get(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)

        response = self.client.get(reverse("add_new_team", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a New Team")

    def test_add_new_sport_post(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)

        response = self.client.post(reverse("add_new_team", args=(Sport.objects.get(name="Football0").name_slug,)),
        data={'name': 'test', 'description': 'test description', 'location': 'test location', 'initial_role': '0'})

        self.assertRedirects(response, reverse("show_team", args=("test",)))
        self.assertEqual(response.status_code, 302)

class ManageTeamTests(TestCase):
    def test_manage_team_not_logged(self):
        create_footballs(count=1)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager")], count=1)
        response = self.client.get(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 302)

    def test_manage_team_not_owner(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager")], count=1)

        response = self.client.get(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_information"))

    def test_manage_team_owner_get(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=1)

        response = self.client.get(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage FootballTeam0")
        self.assertContains(response, "Delete team")

    def test_manage_team_member_get(self):
        user = create_full_user_and_login(self.client)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager"), (user, "goalkeeper")], count=1)

        response = self.client.get(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage FootballTeam0")
        self.assertContains(response, "Leave team")

    def test_manage_team_owner_post(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, [(user, "manager")], count=1)

        response = self.client.post(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)), data={'action': 'Delete team'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_information"))
        self.assertFalse(Team.objects.filter(name="FootballTeam0").exists())

    def test_manage_team_member_post(self):
        user = create_full_user_and_login(self.client)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), dummy_user, [(dummy_user, "manager"), (user, "goalkeeper")], count=1)

        response = self.client.post(reverse("manage_team", args=(Team.objects.get(name="FootballTeam0").name_slug,)), data={'action': 'Leave team'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_information"))
        self.assertTrue(Team.objects.filter(name="FootballTeam0").exists())
        self.assertFalse(TeamUserMembership.objects.filter(user=user, team=Team.objects.get(name="FootballTeam0")).exists())


class ManageSportTests(TestCase):
    def test_manage_sport_not_logged(self):
        create_footballs(count=1)
        response = self.client.get(reverse("manage_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 302)

    def test_manage_sport_not_author(self):
        user = create_full_user_and_login(self.client)
        create_dummy_users(count=1)
        dummy_user = User.objects.get(username="dummy0").userprofile
        create_footballs(user=dummy_user, count=1)

        response = self.client.get(reverse("manage_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_information"))

    def test_manage_sport_get(self):
        user = create_full_user_and_login(self.client)
        create_footballs(user=user, count=1)

        response = self.client.get(reverse("manage_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Football0")

    def test_manage_sport_post(self):
        user = create_full_user_and_login(self.client)
        create_footballs(user=user, count=1)

        response = self.client.post(reverse("manage_sport", args=(Sport.objects.get(name="Football0").name_slug,)), data={'action': 'Delete sport'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_information"))
        self.assertFalse(Sport.objects.filter(name="Football0").exists())

