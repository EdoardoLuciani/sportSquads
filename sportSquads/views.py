from django.shortcuts import render
from django.http import HttpResponse

from sportSquads.models import Sport
from sportSquads.models import Team

from sportSquads.forms import UserForm, UserProfileForm
#from django.shortcuts import redirect

from django.urls import reverse


def home(request):

    sport_list = Sport.objects.all()
    team_list =  Team.objects.all()
    context_dict = {}
    # key boldmessage matches to {{ boldmessage }} in the template
    #context_dict['boldmessage']='Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['sports']=sport_list
    context_dict['teams']=team_list
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    
    response = render(request, "sportSquads/home.html", context=context_dict)

    return response

def show_sport(request,sport_name_slug):
    #context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        sport = Sport.objects.get(slug=sport_name_slug)

        #retrieve all of the associated pages.
        #the filter() will return a list of page objects or an empty list
        teams = team.objects.filter(team=team)

        #Adds our results list to the template context under name pages.
        context_dict['sports'] = sports
        #We also add the category objects from
        #the database to the context dictionary
        #We'll use this in the template to verify that the category exists.
        context_dict['teams'] = teams
        
    except Sport.DoesNotExist:
        #we get here if we didnt find the specified category
        #dont do anything -
        #the template will display "no categort" message
        context_dict['sport']=None
        context_dict['teams']=None

    #Go render the response and return it to the client.
    return render(request, 'sportSquads/sport.html', context=context_dict)


def allsports(request):

    sport_list = Sport.objects.all()
    context_dict = {}
    context_dict['sports']=sport_list
    
    response = render(request, "sportSquads/allsports.html", context=context_dict)

    return response
    
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