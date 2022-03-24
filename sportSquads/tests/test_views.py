from doctest import testfile
import json
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

def create_football_teams(sport, manager, initial_role, count=300):
    available_roles_json = sport.roles.copy()
    available_roles_json[initial_role] = str(int(available_roles_json[initial_role]) - 1)

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
        TeamUserMembership.objects.create(user=manager, team=team, role=initial_role)

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
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=10)

        response = self.client.get(reverse("show_sport", args=(Sport.objects.get(name="Football0").name_slug,)))
        self.assertEqual(response.status_code, 200)
        for i in range(0, 10):
            self.assertContains(response, "FootballTeam" + str(i))

class ShowSportGet10MoreTeamsTests(TestCase):
    def test_show_sport_get_10_more_teams(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=20)

        response = self.client.get(reverse("sport_get_teams", args=(Sport.objects.get(name="Football0").name_slug, 3,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["teams"]), 10)
        for i,data in enumerate(response_data["teams"]):
            self.assertEqual(data["name"], "FootballTeam" + str(i+3))

    def test_show_sport_get_10_more_teams_end(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=10)

        response = self.client.get(reverse("sport_get_teams", args=(Sport.objects.get(name="Football0").name_slug, 10000,)))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(str(response.content, encoding='utf8'))

        self.assertEqual(len(response_data["teams"]), 0)

    def test_show_sport_get_10_more_teams_near_end(self):
        user = create_full_user_and_login(self.client)

        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=10)

class SearchTeamsTests(TestCase):
    def test_name_query(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=30)

        response = self.client.post(reverse("search_teams"), data={'search_text': 'FootballTeam0', 'filters_team_name': ['1']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FootballTeam0")
        self.assertNotContains(response, "FootballTeam1")

    def test_sport_query(self):
        user = create_full_user_and_login(self.client)
        create_footballs(count=1)
        create_football_teams(Sport.objects.get(name="Football0"), user, "manager", count=30)

        response = self.client.post(reverse("search_teams"), data={'search_text': 'Football', 'filters_team_name': ['4']})
        self.assertEqual(response.status_code, 200)
        for i in range(0, 30):
            self.assertContains(response, "FootballTeam" + str(i))