from django.shortcuts import render
from sportSquads.models import Sport,Team


def home(request):
    sport_list = Sport.objects.all()
    team_list =  Team.objects.all()

    context_dict = {}
    context_dict['sports']=sport_list
    context_dict['teams']=team_list

    return render(request, "sportSquads/home.html", context=context_dict)


def show_sport(request, sport_name_slug):
    context_dict = {}
    return render(request, 'sportSquads/sport.html', context=context_dict)


def all_teams(request):
    context_dict = {}
    context_dict['teams'] = Team.objects.all()
    
    return render(request, "sportSquads/all_teams.html", context=context_dict)


def show_team(request, team_name_slug):
    context_dict = {}
    return render(request, 'sportSquads/team.html', context=context_dict)