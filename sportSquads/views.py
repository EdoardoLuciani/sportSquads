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
    add_user_info_to_context(request, context_dict)

    if request.method == 'POST':
        search_sport_form = SearchSportForm(request.POST)

        if search_sport_form.is_valid() and search_sport_form.cleaned_data['search_text']:
            context_dict['search_sport_form'] = search_sport_form
            context_dict['sports'] = Sport.objects.filter(name__icontains=search_sport_form.cleaned_data['search_text'])
            context_dict['searching'] = True
            return render(request, "sportSquads/home.html", context=context_dict)
    
    context_dict['sports'] = Sport.objects.all()[:10]
    context_dict['search_sport_form'] = SearchSportForm()
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


def search_teams(request):
    if request.method == 'POST':
        search_teams_form = SearchTeamForm(request.POST)
        if search_teams_form.is_valid():
            form_filters_list = search_teams_form.cleaned_data['filters_team_name']
            
            teams_query_set = Team.objects.none()
            if '1' in form_filters_list:
                teams_query_set |= Team.objects.filter(name__icontains=search_teams_form.cleaned_data['search_text'])
            if '2' in form_filters_list:
                teams_query_set |= Team.objects.filter(description__icontains=search_teams_form.cleaned_data['search_text'])
            if '3' in form_filters_list:
                teams_query_set |= Team.objects.filter(location__icontains=search_teams_form.cleaned_data['search_text'])
            if '4' in form_filters_list:
                teams_query_set |= Team.objects.filter(sport__name__icontains=search_teams_form.cleaned_data['search_text'])

            context_dict = {
                'search_teams_form' : search_teams_form,
                'teams' : teams_query_set
            }
            return render(request, "sportSquads/search_teams.html", context=context_dict)
    
    context_dict = {
        'search_teams_form' : SearchTeamForm(initial = {'filters_team_name': search_teams_form_filters[0]})
    }
    
    add_user_info_to_context(request, context_dict)        
    return render(request, "sportSquads/search_teams.html", context=context_dict)


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
    context_dict['team'] = Team.objects.get(name_slug=team_name)
    add_user_info_to_context(request, context_dict)

    if request.method == 'POST':
        form = JoinTeamForm(team=context_dict['team'], user=context_dict['user_info'], data=request.POST)

        if form.is_valid():
            form.save()
            context_dict['member'] = True
            return render(request, 'sportSquads/join_team.html', context=context_dict)
        else:
            print(form.errors)
    else:
        try:
            for member in context_dict['team'].teamusermembership_set.all():
                if member.user == context_dict['user_info']:
                    context_dict['member'] = True
                    break
            
            if 'member' not in context_dict and not next((v for v in context_dict['team'].available_roles.values() if v != '0'), None):
                context_dict['full'] = True
            
            context_dict['form'] = JoinTeamForm(user=context_dict['user_info'], team=context_dict['team'])

        except Exception as e:
            print(e)        

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
        form = SportForm(author=user_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('show_sport', args=(slugify(request.POST['name']),)))
        else:
            print(form.errors)

    return render(request, "sportSquads/add_new_sport.html",context = context_dict)


@login_required
def add_new_team(request, sport_name_slug):
    user_profile = UserProfile.objects.get(user=request.user)
    sport = Sport.objects.get(name_slug=sport_name_slug)

    if request.method == 'POST':
        form = TeamForm(manager=user_profile, sport=sport, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse('show_team', args=(slugify(request.POST['name']),)))
        else:
            print(form.errors)

    context_dict = {'form': TeamForm(manager=user_profile, sport=sport),
                    'sport_name_slug': sport_name_slug}

    add_user_info_to_context(request, context_dict)
    return render(request, "sportSquads/add_new_team.html", context=context_dict)


@login_required
def manage_team(request, team_name_slug):
    context_dict = {}
    add_user_info_to_context(request, context_dict)
    context_dict['team'] = Team.objects.get(name_slug=team_name_slug)
    
    if request.method == 'POST':
        manage_team_form = ManageTeamForm(user=context_dict['user_info'], team=context_dict['team'], data=request.POST)
        if (manage_team_form.is_valid()):
            manage_team_form.save()
        return redirect(reverse('account_information'))
    else:
        try:
            context_dict['manage_team_form'] = ManageTeamForm(user=context_dict['user_info'], team=context_dict['team'])
            return render(request, "sportSquads/manage_team.html", context=context_dict)
        except:
            return redirect(reverse('account_information'))

@login_required
def manage_sport(request, sport_name_slug):
    context_dict = {}
    add_user_info_to_context(request, context_dict)
    context_dict['sport'] = Sport.objects.get(name_slug=sport_name_slug)

    if (request.method == 'POST'):
        manage_sport_form = ManageSportForm(user=context_dict['user_info'], sport=context_dict['sport'], data=request.POST)
        if (manage_sport_form.is_valid()):
            manage_sport_form.save()
        return redirect(reverse('account_information'))
    else:
        try:
            context_dict['manage_sport_form'] = ManageSportForm(user=context_dict['user_info'], sport=context_dict['sport'])
            return render(request, "sportSquads/manage_sport.html", context=context_dict)
        except:
            return redirect(reverse('account_information'))