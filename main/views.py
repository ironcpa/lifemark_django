from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from .models import Lifemark
from .forms import LifemarkForm


def get_distinct_categories():
    qset = Lifemark.objects.values('category').distinct()
    category_list = [e['category'] for e in qset]

    if '' not in category_list:
        category_list.append('')

    return sorted(category_list)


def home_page(request):
    lifemarks = (Lifemark.objects
                         .order_by('-udate')[:10])
    existing_categories = get_distinct_categories()

    form = LifemarkForm()
    return render(request, 'home.html', {
        'lifemarks': lifemarks,
        'existing_categories': existing_categories,
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
