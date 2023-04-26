from django.urls import path
from .views import *
app_name = "authors"

urlpatterns = [
   path('posts/', PostsList.as_view(), name="posts"),
   path('search/', PostsSearch.as_view(), name="search"),
   path('post/', PostDetail.as_view(), name="post"),
   #
   path('create/', NewsCreate.as_view(), name='create'),
   # path('article/create/', NewsCreate.as_view(), name='article-create'),

   # path('news/edit/<int:pk>', PostFormView.as_view(), name='news-edit'),
   # path('article/edit/<int:pk>', PostFormView.as_view(), name='article-edit'),

   # path('news/delete/<int:pk>', PostDeleteView.as_view(), name='news-delete'),
   # path('article/delete/<int:pk>', PostDeleteView.as_view(), name='article-delete'),
]
