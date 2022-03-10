from django.shortcuts import render
from django.http import JsonResponse
from sportSquads.forms import UserForm, UserProfileForm
from sportSquads.models import Sport,Team

def home(request):
    sport_list = Sport.objects.all()[:10]

    context_dict = {}
    context_dict['sports'] = sport_list

    return render(request, "sportSquads/home.html", context=context_dict)

def home_get_10_more_sports(request, starting_idx):
    sport_list = (Sport.objects.all()[starting_idx: 10 + starting_idx]).values()
    return JsonResponse({'sports': list(sport_list)})


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
    
def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    
    return render(request, 'sportSquads/sign_up.html', context = {
        'user_form' : user_form,
        'user_profile_form' : user_profile_form,
        'registered' : registered})
