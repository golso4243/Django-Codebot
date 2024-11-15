from django.shortcuts import render

# Home View - This is the home page


def home(request):
    return render(request, 'home.html', {})
