from django import forms

from sportSquads.models import Sport, Team, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SportForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.author = kwargs.pop('author', None)
        super(SportForm, self).__init__(**kwargs)

        self.fields['role_0'] = forms.CharField(max_length=64, required=False)
        self.fields['role_0_count'] = forms.IntegerField(min_value=1, required=False)
        
        if 'data' in kwargs:
            i = 0
            while f'role_{i}' in kwargs['data']:
                i += 1
                self.fields[f'role_{i}'] = forms.CharField(max_length=64, required=False)
                self.fields[f'role_{i}_count'] = forms.IntegerField(min_value=1, required=False)

    def clean(self):
        roles = {}

        i = 0
        while f'role_{i}' in self.cleaned_data:
            role_name = self.cleaned_data[f'role_{i}']
            role_count =  self.cleaned_data[f'role_{i}_count']
            if role_name and role_count:
                roles[role_name] = role_count
            i += 1

        self.cleaned_data['roles'] = roles

    def save(self, commit=True):
        obj = super(SportForm, self).save(commit=False)
        obj.author = self.author
        obj.roles = self.cleaned_data['roles']
        if commit:
            obj.save()
        return obj


    class Meta:
        model = Sport
        fields = ('name', 'image', 'description')


class TeamForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.author = kwargs.pop('author', None)
        super(TeamForm, self).__init__(**kwargs)

        self.fields['role_0'] = forms.CharField(max_length=64, required=False)
        self.fields['role_0_count'] = forms.IntegerField(min_value=1, required=False)
        
        if 'data' in kwargs:
            i = 0
            while f'role_{i}' in kwargs['data']:
                i += 1
                self.fields[f'role_{i}'] = forms.CharField(max_length=64, required=False)
                self.fields[f'role_{i}_count'] = forms.IntegerField(min_value=1, required=False)
    def clean(self):
        roles={}
        i = 0
        while f'role_{i}' in self.cleaned_data:
            role_name = self.cleaned_data[f'role_{i}']
            role_count =  self.cleaned_data[f'role_{i}_count']
            if role_name and role_count:
                roles[role_name] = role_count
            i += 1

        self.cleaned_data['roles'] = roles

    def save(self, commit=True):
        obj = super(SportForm, self).save(commit=False)
        obj.author = self.author
        obj.roles = self.cleaned_data['roles']
        if commit:
            obj.save()
        return obj


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
        
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
