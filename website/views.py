from django.shortcuts import render, redirect
from django.contrib import messages
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Home View - This is the home page


def home(request):
    """
    Handles the home page for both GET and POST requests.
    - GET: Renders the initial form with no data.
    - POST: Processes the code and programming language input,
            sends the code to the OpenAI API for fixing, and
            returns the response to the user.
    """

    # Language list for the dropdown
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    # If the request method is POST
    if request.method == "POST":

        # Get the code and language from the form
        code = request.POST['code']
        lang = request.POST['lang']

        # If the language is not selected
        if lang == 'Select Programming Language':
            # Display a warning message
            messages.warning(request, 'Please select a language')
            return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        # If the language is selected
        else:
            # Create an OpenAI client with the API key
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            try:
                # Send the code to the OpenAI API for fixing
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Fix my {lang} code responding only with the fixed code. Code: {code}.",
                        }
                    ],
                )
                # Save the code and language to the database
                code_obj = Code(question=code, code_answer=response.choices[0].message.content.strip(
                ), language=lang, user=request.user)
                code_obj.save()

                # Return the response to the user
                return render(request, 'home.html', {'lang_list': lang_list, 'response': response.choices[0].message.content.strip(), 'lang': lang})
            # Exception handling
            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'code': e, 'lang': lang})

    # If the request method is GET
    return render(request, 'home.html', {'lang_list': lang_list})


# Suggest View - This is the suggest code page


def suggest(request):
    """
    Handles the suggest page for both GET and POST requests.
    - GET: Renders the initial form with no data.
    - POST: Processes the code input and language, sends it
            to the OpenAI API for suggestions, and displays
            the generated recommendations to the user.
    """

    # language list for the dropdown
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    # if request method is POST
    if request.method == "POST":

        # get code and language from the form
        code = request.POST['code']
        lang = request.POST['lang']

        # if language is not selected
        if lang == 'Select Programming Language':
            # display a warning message
            messages.warning(request, 'Please select a language')
            return render(request, 'suggest.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        # if language is selected
        else:
            # create an OpenAI client with the API key
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            try:
                # send the code to the OpenAI API for suggestions
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Respond only with code in {lang} language: {code}.",
                        }
                    ],
                )
                # Save the code and language to the database
                code_obj = Code(
                    question=code, code_answer=response.choices[0].message.content, language=lang, user=request.user)
                code_obj.save()

                # return the response to the user
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': response.choices[0].message.content.strip(), 'lang': lang})
            # exception handling
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'code': e, 'lang': lang})

    # if request method is GET
    return render(request, 'suggest.html', {'lang_list': lang_list})


# Login View - This is the login page


def login_user(request):
    # if the request method is POST
    if request.method == "POST":
        # get the username and password from the form
        username = request.POST['username']
        password = request.POST['password']
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        # if user is not None
        if user is not None:
            # login the user
            login(request, user)
            # Login Success Message
            messages.success(request, 'You have been logged in successfully!')
            # redirect to the home page
            return redirect('home')
        else:
            # Invalid Login Message
            messages.warning(request, 'Invalid username or password')
            # redirect to the home page
            return redirect('home')
    # if the request method is GET
    else:
        # render the home page
        return render(request, 'home.html')


# Logout View - This is the logout page


def logout_user(request):
    # logout the user
    logout(request)
    # Logout Success Message
    messages.success(request, 'You have been logged out successfully!')
    # redirect to the home page
    return redirect('home')


# Register View - This is the register page


def register_user(request):
    # if the request method is POST
    if request.method == "POST":
        # get the form data
        form = SignUpForm(request.POST)
        # if the form is valid
        if form.is_valid():
            # save the form
            form.save()
            # get the cleaned username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Registration Success Message
            messages.success(request, 'You have been registered successfully!')
            # authenticate the user
            user = authenticate(request, username=username, password=password)
            # login the user
            login(request, user)
            # redirect to the home page
            return redirect('home')
    # if the request method is GET
    else:
        # create a new form
        form = SignUpForm()
    # render the register page
    return render(request, 'register.html', {'form': form})


# History View - This is the history page


def history(request):
    if request.user.is_authenticated:
        code = Code.objects.all().filter(user_id=request.user.id)
        return render(request, 'history.html', {'code': code})
    else:
        messages.warning(request, 'Please login to view your history')
        return redirect('home')
