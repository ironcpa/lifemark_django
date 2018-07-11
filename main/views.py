from django.shortcuts import redirect, render
from django.http import HttpResponse
from main.models import Lifemark
from main.forms import LifemarkForm


def home_page(request):
    if request.method == 'POST':
        form = LifemarkForm(data=request.POST)
        if form.is_valid():
            '''
            Lifemark.objects.create(
                title=request.POST.get('title'),
                link=request.POST.get('link'),
            )
            '''
            form.save()
            return redirect('/')

    lifemarks = Lifemark.objects.all()
    form = LifemarkForm()
    return render(request, 'home.html', {
        'lifemarks': lifemarks,
        'form': form,
    })
