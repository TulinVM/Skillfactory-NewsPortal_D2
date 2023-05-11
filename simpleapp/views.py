from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from authors.filters import PostFilter
from authors.forms import PostForm
from authors.models import Post


class ProductsList(ListView):
    model = Post
    ordering = 'name'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
