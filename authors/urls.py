from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
from django.contrib import admin
app_name = "authors"

urlpatterns = [
   path('', cache_page(3 * 1)(PostsList.as_view()), name='home'),
   path('admin/', cache_page(3 * 1)(PostsList.as_view()), name='admin'),
   path('PostList/', AuthorList.as_view(), name="post_list"),
   path('posts/', PostsList.as_view(), name="posts"),
   path('search/', PostsSearch.as_view(), name="search"),
   # path('post/', PostDetail.as_view(), name="post"),
   # path('news/', PostDetail.as_view(), name="news"),
   path('create/', NewsCreate.as_view(), name='create'),
   path('News-Create/', NewsCreate.as_view(), name='news-create'),
   path('article/create/', NewsCreate.as_view(), name='article-create'),
   path('post/<int:pk>', PostDetail.as_view(), name='post'),
   path('news/edit/<int:pk>', PostFormView.as_view(), name='news-edit'),
   path('article/edit/<int:pk>', PostFormView.as_view(), name='article-edit'),
   path('news/delete/<int:pk>', PostDeleteView.as_view(), name='news-delete'),
   path('article/delete/<int:pk>', PostDeleteView.as_view(), name='article-delete'),
   path('/admin/', admin.site.urls),
   ]