from django.shortcuts import render
from django.http import HttpResponse


from sportSquads.models import Sport
from sportSquads.models import Team


#from sportSquads.forms import CategoryForm
#from django.shortcuts import redirect

from django.urls import reverse

# Create your views here.

def home(request):

    sport_list =  Sport.objects
    team_list =  Team.objects
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
