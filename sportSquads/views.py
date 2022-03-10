from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from sportSquads.forms import *
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


def user_login(request):
    if request.method == 'POST':
        user_login_form = AuthenticationForm(request, data=request.POST)
        
        if user_login_form.is_valid():
            user = authenticate(username=user_login_form.cleaned_data['username'], password=user_login_form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse("Invalid login details")
        else:
            return HttpResponse("Invalid login details")

    return render(request, 'sportSquads/login.html', context= { 'user_login_form' : AuthenticationForm()})    


def contact_us(request):
    return render(request, 'sportSquads/contact_us.html')
    
