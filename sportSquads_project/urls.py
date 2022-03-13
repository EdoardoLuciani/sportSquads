"""sportSquads_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sportSquads import views
from django.urls import include

app_name = 'sportSquads'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('home_get_10_more_sports/<int:starting_idx>', views.home_get_10_more_sports, name='home_get_sports'),

    path('sign-up', views.sign_up, name='sign_up'),
    path('all-teams', views.all_teams, name='all_teams'),
    path('contact-us', views.contact_us, name='contact_us'),
    path('login/', views.user_login, name='login'),
    path('sport/<slug:sport_name_slug>/', views.show_sport, name='show_sport'),
    path('sport_get_10_more_teams/<int:starting_team_no>/<slug:sport_name>', views.sport_get_10_more_teams, name='sport_get_teams'),

    path('team/<slug:team_name_slug>/', views.show_team, name='show_team'),
    path('account', views.account_information, name='account_information'),
    path('add-sport/', views.add_new_sport, name='add_new_sport'),
    path('logout/', views.user_logout, name='logout'),
    
]
