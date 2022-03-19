from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from sportSquads.forms import *
from sportSquads.models import Sport, Team, UserProfile
from django.contrib.auth.decorators import login_required

def add_user_info_to_context(request, context_dict):
    try:
        context_dict['user_info'] = UserProfile.objects.get(user=request.user)
    except:
        context_dict['user_info'] = None


def home(request):
    context_dict = {}
    context_dict['sports'] = Sport.objects.all()[:10]
    add_user_info_to_context(request, context_dict)
    return render(request, "sportSquads/home.html", context=context_dict)


def home_get_10_more_sports(request, starting_idx):
    sport_list = (Sport.objects.all()[starting_idx: 10 + starting_idx]).values()
    return JsonResponse({'sports': list(sport_list)})

@login_required
def account_information(request):
    context_dict = {}
    add_user_info_to_context(request, context_dict)
    return render(request, "sportSquads/account_information.html", context=context_dict)
    
def show_sport(request, sport_name_slug):
    context_dict = {}
    
    try:
        context_dict['sport'] = Sport.objects.get(name_slug=sport_name_slug)
        context_dict['teams'] = Team.objects.filter(sport=context_dict['sport'])[:10]
    except:
        pass
    
    add_user_info_to_context(request, context_dict)
    return render(request, 'sportSquads/sport.html', context=context_dict)


def sport_get_10_more_teams(request, sport_name, starting_team_no):
    sport_name = Sport.objects.get(name_slug=sport_name)
    teams = (Team.objects.filter(sport=sport_name)[starting_team_no: 10 + starting_team_no]).values()
    return JsonResponse({'teams': list(teams)})


def all_teams(request):
    if request.method == 'POST':
        search_team_form = SearchTeamForm(request.POST)
        if search_team_form.is_valid():
            form_filters_list = search_team_form.cleaned_data['filters_team_name']
            
            teams_query_set = Team.objects.none()
            if '1' in form_filters_list:
                teams_query_set |= Team.objects.filter(name__icontains=search_team_form.cleaned_data['search_text'])
            if '2' in form_filters_list:
                teams_query_set |= Team.objects.filter(description__icontains=search_team_form.cleaned_data['search_text'])
            if '3' in form_filters_list:
                teams_query_set |= Team.objects.filter(location__icontains=search_team_form.cleaned_data['search_text'])
            if '4' in form_filters_list:
                teams_query_set |= Team.objects.filter(sport__name__icontains=search_team_form.cleaned_data['search_text'])

            context_dict = {
                'search_team_form' : search_team_form,
                'teams' : teams_query_set
            }
            return render(request, "sportSquads/all_teams.html", context=context_dict)
    
    context_dict = {
        'search_team_form' : SearchTeamForm(initial = {'filters_team_name': search_team_form_filters[0]})
    }
    
    add_user_info_to_context(request, context_dict)        
    return render(request, "sportSquads/all_teams.html", context=context_dict)


def show_team(request, team_name_slug):
    context_dict = {}
    try:
        context_dict['team'] = Team.objects.get(name_slug=team_name_slug)
    except:
        pass

    add_user_info_to_context(request, context_dict)
    return render(request, 'sportSquads/team.html', context=context_dict)


@login_required
def join_team(request, team_name):
    context_dict = {}

    try:
        already_member = False
        context_dict['team'] = Team.objects.get(name_slug=team_name)
        context_dict['user'] = UserProfile.objects.get(user=request.user)
        roles = context_dict['team'].available_roles

        for member in context_dict['team'].teamusermembership_set.all():
            if member.user == context_dict['user']:
                already_member = True
                break
        
        context_dict['member'] = already_member
        context_dict['form'] = JoinTeamForm(roles)

    except:
        pass

    if request.method == 'POST':
        form = JoinTeamForm(team=context_dict['team'], roles=roles, data=request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            context_dict['member'] = True
            return render(request, 'sportSquads/join_team.html', context=context_dict)
        else:
            print(form.errors)

    return render(request, 'sportSquads/join_team.html', context=context_dict)


def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            registered = True

            login(request, user)
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
            user = authenticate(username=user_login_form.cleaned_data['username'],
                                password=user_login_form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    return HttpResponse("Your account has been disabled")
        else:
            return HttpResponse("Invalid login details")

    return render(request, 'sportSquads/login.html', context={'user_login_form': AuthenticationForm()})    


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


def contact_us(request):
    context_dict = {}
    add_user_info_to_context(request, context_dict)
    return render(request, 'sportSquads/contact_us.html', context=context_dict)


@login_required
def add_new_sport(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict = {'form': SportForm(author=user_profile)}
    add_user_info_to_context(request, context_dict)

    if request.method == 'POST':
        form = SportForm(author=user_profile, data=request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect(reverse('home'))
        else:
            print(form.errors)

    return render(request, "sportSquads/add_new_sport.html",context = context_dict)


@login_required
def add_new_team(request, sport_name):
    user_profile = UserProfile.objects.get(user=request.user)
    sport = Sport.objects.get(name=sport_name)

    if request.method == 'POST':
        form = TeamForm(manager=user_profile, sport=sport, available_roles=sport.roles,
                        data=request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect(reverse('home'))
        else:
            print(form.errors)
    context_dict = {'form': TeamForm(manager=user_profile, sport=sport),
                    'sport_name': sport_name}
                    
    add_user_info_to_context(request, context_dict)
    return render(request, "sportSquads/add_new_team.html", context=context_dict)

