from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User

# Модель, содержащая объекты всех авторов
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        articles_rate = Post.objects.filter(author_id=self.pk).aggregate(sum_articles=Sum('post_rating'))['post_rating'] * 3
        comments_rate = Comment.objects.filter(users_id=self.author).aggregate(sum_articles=Sum('comment_rating'))['comment_rating']
        comments_articles_rate = Comment.objects.filter(post__author__users=self.author).aggregate(sum_posts=Sum('comment_rating'))['comment_rating']
        self.author_rating = articles_rate + comments_rate + comments_articles_rate
        self.save()

sport = 'SP'
education = 'ED'
policy = 'PO'
economy = 'EC'

TOPICS = [
    (sport, 'Спорт'),
    (education, 'Образование'),
    (policy, 'Политика'),
    (economy, 'Экономика')
]

# Категории новостей/статей — темы, которые они отражают
class Category(models.Model):
    category = models.CharField(max_length=55, unique=True)

news = 'NE'
articles = 'AR'

TYPES = [
    (news, 'Новости'),
    (articles, 'Статьи'),
]

# модель, содержащая статьи и новости, которые создают пользователи
class Post(models.Model):
    post_autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPES, default=news)
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_header = models.CharField(max_length=125)
    post_text = models.TextField(blank=False)
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        dots = self.post_text
        return dots[0:124] + '...'

# Промежуточная модель для связи «многие ко многим»
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

# Модель для хранения комментариев к постам
class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        if self.comment_rating >= 0:
            self.comment_rating += 1
            self.save()

    def dislike(self):
        if self.comment_rating > 0:
            self.comment_rating -= 1
            self.save()
