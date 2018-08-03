from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from .models import Lifemark
from .forms import LifemarkForm


def home_page(request):
    lifemarks = Lifemark.objects.all()

    for lifemark in lifemarks:
        print(lifemark.id, lifemark.desc)

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

    return redirect(reverse_lazy('home'))


class CreateLifemarkView(CreateView):
    model = Lifemark
    form_class = LifemarkForm
    template_name = 'home.html'
    # below code failed w/ no reason i can catch!
    # success_url = reverse('home')
    success_url = reverse_lazy('home')


def update_lifemark(request):
    if request.method == 'POST':
        target = Lifemark.objects.get(id=request.POST['id'])
        form = LifemarkForm(data=request.POST, instance=target)
        if form.is_valid():
            form.save()
    return redirect(reverse_lazy('home'))


class UpdateLifemarkView(UpdateView):
    model = Lifemark
    # fields = ('title', 'link', 'category', 'is_complete', 'due_datehour',
    #           'rating', 'tags', 'image_url')
    form_class = LifemarkForm
    template_name = 'home.html'
    # below code failed w/ no reason i can catch!
    success_url = reverse_lazy('home')


class DeleteLifemarkView(DeleteView):
    model = Lifemark
    success_url = reverse_lazy('home')


class TestListView(ListView):
    model = Lifemark
    template_name = 'home.html'


class TestUpdateView(UpdateView):
    model = Lifemark
