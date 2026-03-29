from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Category(models.Model):
    """Modelo de Categoria - ManyToMany com Post"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Modelo de Tag - ManyToMany com Post"""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # ForeignKey: Um Post pertence a UM User (Um-para-Muitos)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # ManyToMany: Um Post pode ter VÁRIAS Categorias e vice-versa
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    # ManyToMany: Um Post pode ter VÁRIAS Tags e vice-versa
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Modelo de Comentário - ForeignKey com Post"""
    # ForeignKey: Um Comentário pertence a UM Post (Um-para-Muitos)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # ForeignKey: Um Comentário foi escrito por UM User
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comentário de {self.author.username} em {self.post.title}'
