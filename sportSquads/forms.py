from django import forms

from sportSquads.models import Sport, Team, UserProfile
from django.contrib.auth.models import User

class SportForm(forms.ModelForm):
    name = forms.CharField(max_length=64,
                           help_text="Name of Sport: ")
    image = forms.ImageField(required=False,
                             help_text="Image (Optional)")
    description = forms.CharField(help_text="Description of sport")
    roles = forms.CharField(help_text="roles")

    class Meta:
        model = Sport
        exclude = ('author',)
        fields = ('name', 'image', 'description', 'roles')


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