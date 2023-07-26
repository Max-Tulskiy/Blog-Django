from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED) # super не полностью переопределяет метод объекта


class Post(models.Model):

    objects = models.Manager() #менеджер по умолчанию
    published = PublishedManager() #конкретно-прикладной менеджер

    tags = TaggableManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, #поле указывает, что при удалении пользователя, бд удалит все его посты
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    # динамическое формирование url адреса
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE, # если пост удалится, то из базы удалися вся информация с ним связанная
                             related_name='comments') # обращение из связанных объектов к тем, от которых эта связь была создана

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) # создает метку при создании строки в базе
    updated = models.DateTimeField(auto_now=True) # обновляет метку
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"