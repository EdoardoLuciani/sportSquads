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

    def clean(self):
        roles = {
            'roles' : {}
        }

        i = 0
        while self.cleaned_data.get(f'role_{i}'):
            roles['roles'][self.cleaned_data[f'role_{i}']] = self.cleaned_data[f'role_{i}_count']
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
    pass


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio')