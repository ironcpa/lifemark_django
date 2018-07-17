from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Lifemark
from .forms import LifemarkForm


def home_page(request):
    lifemarks = Lifemark.objects.all()
    form = LifemarkForm()
    return render(request, 'home.html', {
        'lifemarks': lifemarks,
        'form': form,
    })


def new_lifemark(request):
    if request.method == 'POST':
        form = LifemarkForm(data=request.POST)
        if form.is_valid():
            form.save()

    return redirect('/')


def update_lifemark(request):
    if request.method == 'POST':
        target = Lifemark.objects.get(id=request.POST['id'])
        form = LifemarkForm(data=request.POST, instance=target)
        if form.is_valid():
            form.save()
    return redirect('/')
