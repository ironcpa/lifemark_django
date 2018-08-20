from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Lifemark
from .forms import LifemarkForm


def get_distinct_categories():
    qset = Lifemark.objects.values('category').distinct()
    category_list = [e['category'] for e in qset]

    if '' not in category_list:
        category_list.append('')

    return sorted(category_list)


@login_required
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


@login_required
def search(request):
    keyword = request.GET.get('q')
    lifemarks_qs = Lifemark.objects.get_matches_on_fields(
        ('title', 'link', 'category', 'state', 'rating', 'tags', 'desc', 'image_url'),
        keyword
    ).order_by('-udate')

    page_no = request.GET.get('page', 1)
    paginator = Paginator(lifemarks_qs, 10)
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        # fallback to last_page
        page = paginator.page(paginator.num_pages)

    existing_categories = get_distinct_categories()

    form = LifemarkForm()
    return render(request, 'home.html', {
        'lifemarks': page,
        # 'q': keyword,
        'existing_categories': existing_categories,
        'form': form,
    })


@method_decorator(login_required, name='dispatch')
class LifemarkSearchListView(ListView):
    model = Lifemark
    context_object_name = 'lifemarks'
    template_name = 'home.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['existing_categories'] = get_distinct_categories()
        kwargs['form'] = LifemarkForm()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        keyword = self.request.GET.get('q')

        if keyword:
            queryset = Lifemark.objects.get_matches_on_fields(
                ('title', 'link', 'category', 'state', 'rating', 'tags', 'desc', 'image_url'),
                keyword
            ).order_by('-udate')
        else:
            queryset = Lifemark.objects.all().order_by('-udate')

        return queryset


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
