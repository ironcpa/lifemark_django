from django.shortcuts import redirect, render
from django.http import HttpResponse
from main.models import Lifemark


def home_page(request):
    if request.method == 'POST':
        Lifemark.objects.create(title=request.POST['add_title'])
        return redirect('/')

    lifemarks = Lifemark.objects.all()
    return render(request, 'home.html', {'lifemarks': lifemarks})
