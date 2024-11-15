from django.shortcuts import render

# Home View - This is the home page


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'lua', 'markup', 'markup-templating',
                 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']
    return render(request, 'home.html', {'lang_list': lang_list})
