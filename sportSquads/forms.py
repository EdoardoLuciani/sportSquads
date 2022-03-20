from django import forms
from sportSquads.models import *
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
        fields = ('name', 'image', 'description',)


class TeamForm(forms.ModelForm):
    initial_role = forms.CharField(max_length=64, required=True)

    def __init__(self, **kwargs):
        self.manager = kwargs.pop('manager', None)
        self.sport = kwargs.pop('sport', None)
        self.available_roles = kwargs.pop('available_roles', None)
        super(TeamForm, self).__init__(**kwargs)

    def clean(self):        
        if self.cleaned_data['initial_role'] in self.available_roles:
            self.available_roles[self.cleaned_data['initial_role']] -= 1
            self.cleaned_data['available_roles'] = self.available_roles
        else:
            raise forms.ValidationError('Role not available')

    def save(self, commit=True):
        obj = super(TeamForm, self).save(commit=False)
        obj.manager = self.manager
        obj.sport = self.sport
        obj.available_roles = self.cleaned_data['available_roles']
        if commit:
            obj.save()
            team_user_membership = TeamUserMembership(user=self.manager, team=obj, role=self.cleaned_data['initial_role'])
            team_user_membership.save()
        return obj

    class Meta:
        model = Team
        fields = ('name', 'image', 'description', 'location', )



class JoinTeamForm(forms.Form):
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user')
        self.team = kwargs.pop('team')
        super(JoinTeamForm, self).__init__(**kwargs)

        self.roles_list = [('', 'Select Role')]
        for i,elem in enumerate(filter(lambda e: e[1] != '0', self.team.available_roles.items())):
            self.roles_list.append((i, elem[0]))
        self.fields['role'] = forms.TypedChoiceField(choices=self.roles_list, coerce=int)

    def clean_role(self):
        filtered_roles = list(filter(lambda e: e[0] == self.cleaned_data['role'], self.roles_list))
        if len(filtered_roles) == 1:
            return filtered_roles[0][1]
        else:
            raise forms.ValidationError('Role is not available')
    
    def save(self, commit=True):
        if commit:
            member_with_role_relation = TeamUserMembership(
            user=self.user, team=self.team, role=self.cleaned_data['role'])
            member_with_role_relation.save()

            current_role_count = int(self.team.available_roles[self.cleaned_data['role']])
            self.team.available_roles[self.cleaned_data['role']] = str(current_role_count - 1)
            self.team.save()

        return self
        

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
    ('4', 'Sport name')
]
class SearchTeamForm(forms.Form):
    search_text = forms.CharField(label='Write here your search words', max_length=100)
    filters_team_name = forms.MultipleChoiceField(label='Select at least one filter', choices=search_team_form_filters, widget=forms.CheckboxSelectMultiple())
