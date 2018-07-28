from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
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


class CreateLifemarkView(CreateView):
    model = Lifemark
    form_class = LifemarkForm
    template_name = 'home.html'
    # below code failed w/ no reason i can catch!
    # success_url = reverse('home')
    success_url = '/'


def update_lifemark(request):
    if request.method == 'POST':
        target = Lifemark.objects.get(id=request.POST['id'])
        form = LifemarkForm(data=request.POST, instance=target)
        if form.is_valid():
            form.save()
    return redirect('/')


class UpdateLifemarkView(UpdateView):
    model = Lifemark
    # fields = ('title', 'link', 'category', 'is_complete', 'due_datehour',
    #           'rating', 'tags', 'image_url')
    form_class = LifemarkForm
    template_name = 'home.html'
    # below code failed w/ no reason i can catch!
    success_url = reverse_lazy('home')


'''
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter lifemark title',
            }),
            'link': forms.fields.URLInput(attrs={
                'placeholder': 'Enter related page link',
            }),
            'category': forms.fields.HiddenInput(),
            'is_complete': forms.fields.Select(choices=CHOICES_STATE),
            'due_datehour': forms.fields.HiddenInput(),
            'rating': forms.fields.TextInput(),
            'tags': forms.fields.TextInput(),
            'image_url': forms.fields.TextInput(),
        }
        '''

'''
class UpdateLifemarkView(UpdateView):
    model = Lifemark
    form_class = LifemarkForm
    template_name = 'home.html'
    success_url = '/'
    '''


class TestListView(ListView):
    model = Lifemark
    template_name = 'home.html'


class TestUpdateView(UpdateView):
    model = Lifemark
