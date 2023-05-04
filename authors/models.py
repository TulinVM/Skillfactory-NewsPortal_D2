from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User

from . import TYPE_CHOICES

article = 'A'
news = 'N'

Types = [
    (article, 'статья'),
    (news, 'новость'),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        my_posts = self.posts.all()
        post_comments = [p.post_comments.aggregate(sum=Sum('rating'))['sum'] for p in my_posts]
        post_comments = sum(post_comments)
        posts = self.posts.values('rating')
        posts = sum(p['rating'] for p in posts) * 3
        comments = self.user.comments.values('rating')
        comments = sum(c['rating'] for c in comments)
        self.rating = posts + comments + post_comments

class Category(models.Model):
    name = models.CharField(unique=True, max_length=256, verbose_name='Название')


class Post(models.Model):
    article = 'A'
    news = 'N'
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    categories = models.ManyToManyField(Category, verbose_name='Категория')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    title = models.CharField(unique=True, max_length=256, verbose_name='Название')
    text = models.TextField()
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Рейтинг больше, чем')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Создан ранее, чем')


    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text



    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1





class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='Посты' )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Автор', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Рейтинг больше, чем')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Создан ранее, чем')
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1



