"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from peers import views
from webserver import startup
import Config


urlpatterns = [
    path('', views.index, name='index'),
    path('infos', views.InformationView.as_view(), name='information'),
    path('getId', views.GetIdView.as_view(), name='getId'),
    path('generate', views.GenerateView.as_view(), name='generate'),
    path('create', views.CreateVisualsView.as_view(), name='create'),
    path('graph', views.GraphEnterIdView.as_view(), name='enterGraph'),
    path('graph/<int:accountId>', views.GraphView.as_view(), name='graph'),
    path('about', views.AboutView.as_view(), name='about'),
    path('gen/<str:id>', views.GenView.as_view(), name='gen'),
    path('test', views.test, name='test'),

    # Static
    path(f'{Config.PROFILE_PICTURES_FOLDER}/<int:nbr1>/<int:nbr2>/<str:name>', views.ProfilePicturesPath.as_view(), name='profilePictures'),
]

# Execute startup code
startup.onStartup()
