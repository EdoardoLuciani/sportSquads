from django import forms

from sportSquads.models import Sport, Team, UserProfile
from django.contrib.auth.models import User

class SportForm(forms.ModelForm):
    pass

class TeamForm(forms.ModelForm):
    pass

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio')

search_team_form_filters = [
    ('1', 'Team name'),
    ('2', 'Team description'),
    ('3', 'Team location'),
]
class SearchTeamForm(forms.Form):
    search_text = forms.CharField(label='Write here your search words', max_length=100)
    filters_team_name = forms.MultipleChoiceField(label='Select at least one filter', choices=search_team_form_filters, widget=forms.CheckboxSelectMultiple())