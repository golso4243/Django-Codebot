from django.urls import path  # Import the path function from django.urls
from . import views  # Import the views module from the current directory

urlpatterns = [
    path('', views.home, name='home'),  # This is the home page
]
