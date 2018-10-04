from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('home'))
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def sample_view(request):
    return redirect(reverse('home'))


def test_anon_user_view(request):
    # return render(request, 'home.html')
    return redirect(reverse('home'))


def test_create_user(request):
    username = request.GET['username']
    password = request.GET['password']
    User.objects.create_user(
        username=username,
        password=password
    )

    return HttpResponse('create test user')
