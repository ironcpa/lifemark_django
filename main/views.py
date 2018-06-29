from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html', {
        'add_title': request.POST.get('add_title')
    })
