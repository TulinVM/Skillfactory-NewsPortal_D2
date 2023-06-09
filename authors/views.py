################# news from
# импорты django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
# группа импорта для реализации механизма добавления в группу пользователя через реадктирование профиля на портале
# с использованием библиотеки allauth
from django.shortcuts import redirect
from pyexpat.errors import messages

# from .forms import AddPostForm
# from project.simpleapp.models import Product
# импорты проекта
from .models import Post, Author
from .forms import PostForm
from django.contrib.auth.models import User
from .filters import PostFilter
# Настройки включения перевода
from django.utils.translation import gettext as _ # импортируем функцию перевода
# ограничение на количество публикаций в день для автора
LIMIT_POSTS = 20
# пример создания вьюшки через класс - исключительно в целях тестирования реализации перевода


class IndexTrans(View):
    def get(self, request):
        string = _("Test string")
        return HttpResponse(string)


# Пример реализации вьюшки через класс  для обучения настройки изменения таймзоны
class IndexTimezone(View):
    def get(self, request):
        # Код ниже перенесен в контекстынй процессор context_processors.py
        # user_timezone = pytz.timezone(request.session.get('django_timezone') or settings.TIME_ZONE)
        # current_time = timezone.now().astimezone(user_timezone)
        #
        # context = {
        #     'current_time': current_time,
        #     'timezones': pytz.common_timezones #  добавляем в контекст все доступные часовые пояса
        # }
        return HttpResponse(render(request, 'flatpages/default.html', {}))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('index_test')

#######
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'authors.html'
    queryset = Author.objects.all()
    post = ['title', 'text']

class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# class PostDetail(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'
#     queryset = Post.objects.all()

#################
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    #slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context



class PostsSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # def form_valid(self, form):
    #     author = Author.objects.filter(user=self.request.user.id).first()
    #     if not author:
    #         author = Author.objects.first()
    #         messages.error(self.request, "You not author, we get first.")
    #     else:
    #         messages.success(self.request, "The task was created successfully.")
    #     form.instance.author = author
    #     form.instance.type = 'N'
    #
    #     return super(NewsCreate, self).form_valid(form)
################
# class NewsCreate(CreateView):
#     model = Post
#     fields = ['categories', 'title', 'text']
#     template_name = 'addpage.html'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Добавление статьи'
#         context['menu'] = menu
#         return context
#####
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
#

class ArticleCreate(CreateView):
    model = Post
    fields = ['categories', 'title', 'text']
    success_url = reverse_lazy('authors:posts')

    def form_valid(self, form):
        author = Author.objects.filter(user=self.request.user.id).first()
        if not author:
            author = Author.objects.first()
            messages.error(self.request, "You not author, we get first.")
        else:
            messages.success(self.request, "The task was created successfully.")
        form.instance.author = author
        form.instance.type = 'A'

        return super(ArticleCreate, self).form_valid(form)

class PostFormView(UpdateView):
    permission_required = ('simpleapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDeleteView(DeleteView):
    permission_required = ('simpleapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class Post(View):
    model = Post
    success_url = reverse_lazy('authors:post')
    template_name = 'authors/post.html'


def cat_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/cat_detail.html',
         {'category': category, 'products': products, 'page_obj': page_obj})
