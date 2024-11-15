from django.shortcuts import render
from django.contrib import messages

# Home View - This is the home page


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == 'Select Programming Language':
            messages.error(request, 'Please select a language')
            return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
    return render(request, 'home.html', {'lang_list': lang_list})
