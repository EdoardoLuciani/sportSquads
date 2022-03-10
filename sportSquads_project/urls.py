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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('all_teams', views.all_teams, name='all_teams'),
    path('sport/<slug:sport_name_slug>/', views.show_sport, name='show_sport'),
    path('team/<slug:team_name_slug>/', views.show_team, name='show_team'),
    path('add-sport', views.add_new_sport, name='add_new_sport')
]
