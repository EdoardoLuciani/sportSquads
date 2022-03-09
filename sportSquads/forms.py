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