from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy

from .filters import PostFilter
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import PostForm
from .models import *



class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'authors.html'
    queryset = Author.objects.all()

class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
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
        form.instance.type = 'N'

        return super(NewsCreate, self).form_valid(form)


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
    model = Post
    fields = [
        "title",
        "text"
    ]
    success_url = reverse_lazy('authors:posts')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('authors:posts')
    template_name = "authors/confirm_delete.html"