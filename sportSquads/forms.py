from django import forms
from sportSquads.models import Sport,Team
#from sportSquads.models import UserProfile
#from django.contrib.auth.models import User

class SportForm(forms.ModelForm):
    name = forms.CharField(max_length=64,
                           help_text="Please enter the category name.")
    image = forms.ImageField(upload_to='sport_images', blank=True)
    description = forms.TextField()
    author = forms.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    roles = forms.JSONField()
    name_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    

    #An inline class to provide additional info on the form
    class Meta:
        #provide an association between the ModelForm and the form
        model = Sport
        fields = ('name',)


class TeamForm(forms.ModelForm):

    title = forms.CharField(max_length=64,
                            help_text="Please enter the title of the page.")
    image = forms.ImageField(upload_to='team_images', blank=True)
    description = forms.TextField()
    location = forms.CharField(max_length=128)
    sport = forms.ForeignKey(Sport, on_delete=models.PROTECT)
    
    url=forms.URLField(max_length=200,
                             help_text="Please enter the URL of the page.")
    

    class Meta:
        #provide an association between the ModelForm and the form
        model = Team

        #what to include in the form
        #dont need every field in the model present.
        #may not want to include field that allow NULL values
        #Here, we are hiding the foreign key
        #we can exclude the category field from the form
        exclude = ('sport',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        #if url is not empty and doesnt start with http://
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data
        
'''       
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','website',)
'''
