from collections import OrderedDict
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
    param_keyword = request.GET.get('q')
    keywords = param_keyword.split()
    search_fields = ('title',
                     'link',
                     'category',
                     'state',
                     'rating',
                     'tags',
                     'desc',
                     'image_url')
    lifemarks_qs = Lifemark.objects.get_matches_on_fields(
        search_fields,
        keywords
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
        'existing_categories': existing_categories,
        'form': form,
    })


@method_decorator(login_required, name='dispatch')
class LifemarkSearchListView(ListView):
    model = Lifemark
    context_object_name = 'lifemarks'
    template_name = 'home.html'
    paginate_by = 10
    search_fields = ('title',
                     'link',
                     'category',
                     'state',
                     'rating',
                     'tags',
                     'desc',
                     'image_url')

    def get_context_data(self, **kwargs):
        kwargs['existing_categories'] = get_distinct_categories()
        kwargs['form'] = LifemarkForm()

        paged_lifmarks = super().get_context_data()['page_obj']
        kwargs['lifemark_line_data'] = self.get_keywords_lines(
            list(paged_lifmarks),
            self.request.GET.get('q'),
            self.search_fields
        )

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        keywords = self.request.GET.get('q')

        if keywords:
            queryset = Lifemark.objects.get_matches_on_fields(
                self.search_fields,
                keywords
            ).order_by('-udate')
        else:
            queryset = Lifemark.objects.all().order_by('-udate')
            self.search_by_line = []

        return queryset

    def get_keywords_lines(self, lifemarks, keywords_str, search_fieldnames=None):
        if not search_fieldnames:
            search_fieldnames = ()

        if keywords_str:
            keywords = keywords_str.split(' ')
        else:
            keywords = []

        search_line_data = OrderedDict()

        for lm in lifemarks:
            match_lines = []
            for fieldname in search_fieldnames:
                field_lines = getattr(lm, fieldname).split('\r\n')
                for line_no, line in enumerate(field_lines):
                    for keyword in keywords:
                        if line and keyword.lower() in line:
                            match_line_data = (fieldname, line_no, line)
                            if match_line_data not in match_lines:
                                match_lines.append(match_line_data)

            search_line_data[lm.id] = {'lifemark': lm,
                                       'lines': match_lines}

        return search_line_data


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


def test_view(request):
    return '<table><tr><td></td><td>title</td><td>0</td><td>aaa keyword</td></tr></table>'
