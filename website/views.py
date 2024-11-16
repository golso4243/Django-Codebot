from django.shortcuts import render
from django.contrib import messages
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Home View - This is the home page


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == 'Select Programming Language':
            messages.warning(request, 'Please select a language')
            return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Fix my {lang} code responding only with the fixed code. Code: {code}.",
                        }
                    ],
                )
                return render(request, 'home.html', {'lang_list': lang_list, 'response': response.choices[0].message.content.strip(), 'lang': lang})
            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'code': e, 'lang': lang})

    return render(request, 'home.html', {'lang_list': lang_list})


# Suggest View - This is the suggest code page


def suggest(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == 'Select Programming Language':
            messages.warning(request, 'Please select a language')
            return render(request, 'suggest.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Respond only with code in {lang} language: {code}.",
                        }
                    ],
                )
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': response.choices[0].message.content.strip(), 'lang': lang})
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'code': e, 'lang': lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})
