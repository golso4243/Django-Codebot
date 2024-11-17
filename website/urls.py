from django.urls import path  # Import the path function from django.urls
from . import views  # Import the views module from the current directory

urlpatterns = [
    # This is the home page
    path('', views.home, name='home'),
    # This is the suggest code page
    path('suggest/', views.suggest, name='suggest'),
    # This is the login page
    path("login/", views.login_user, name="login"),
    # This is the logout page
    path("logout/", views.logout_user, name="logout"),
    # This is the register page
    path("register/", views.register_user, name="register"),
    # This is the history page
    path('history/', views.history, name='history'),
]
