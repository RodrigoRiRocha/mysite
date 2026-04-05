# models.py — define as tabelas do banco de dados usando classes Python.
# Cada classe que herda de models.Model vira uma tabela no banco.
# O Django lê esses modelos e gera as migrações (arquivos SQL) automaticamente.

from django.db import models
from django.contrib.auth.models import User  # Modelo de usuário já embutido no Django


class PostStatus(models.IntegerChoices):
    """
    Choices for Post status using Django's IntegerChoices.
    Provides better type safety and IDE autocomplete compared to magic tuple values.
    """
    DRAFT = 0, 'Draft'       # 0 = rascunho, não aparece no site
    PUBLISHED = 1, 'Published'  # 1 = publicado, visível para os visitantes


class Category(models.Model):
    # Categoria serve para agrupar posts por tema (ex: Python, Django, etc.)
    # A relação com Post é ManyToMany: um post pode ter várias categorias
    # e uma categoria pode ter vários posts.

    name = models.CharField(max_length=100, unique=True)  # unique=True impede categorias duplicadas
    description = models.TextField(blank=True)            # blank=True torna o campo opcional
    created_on = models.DateTimeField(auto_now_add=True)  # preenchido automaticamente na criação

    class Meta:
        verbose_name_plural = 'Categories'  # nome no admin (evita "Categorys")
        ordering = ['name']                 # lista sempre em ordem alfabética

    def __str__(self):
        # Define o que aparece quando você imprime ou exibe o objeto (ex: no admin)
        return self.name


class Tag(models.Model):
    # Tag é uma etiqueta livre para classificar posts (ex: ORM, Tutorial, API).
    # Relação com Post também é ManyToMany.

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    # Post é o modelo principal do blog — representa um artigo.

    title = models.CharField(max_length=200, unique=True)  # título único do post
    slug = models.SlugField(max_length=200, unique=True)   # versão do título para a URL (ex: meu-primeiro-post)

    # ForeignKey = relação Um-para-Muitos: um User pode ter VÁRIOS posts,
    # mas cada post pertence a UM autor.
    # on_delete=CASCADE: se o usuário for deletado, seus posts também são deletados.
    # related_name='blog_posts': permite acessar os posts de um usuário via user.blog_posts.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # ManyToManyField = relação Muitos-para-Muitos:
    # um post pode ter VÁRIAS categorias e uma categoria pode ter VÁRIOS posts.
    # related_name='posts': permite acessar os posts de uma categoria via category.posts.all()
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)

    # Mesmo conceito para tags
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    updated_on = models.DateTimeField(auto_now=True)      # atualizado automaticamente a cada save()
    content = models.TextField()                          # conteúdo do post (texto longo)
    created_on = models.DateTimeField(auto_now_add=True)  # preenchido na criação, nunca muda
    status = models.IntegerField(choices=PostStatus, default=PostStatus.DRAFT)  # Draft ou Published

    class Meta:
        ordering = ['-created_on']  # '-' = ordem decrescente (posts mais novos primeiro)

    def __str__(self):
        return self.title
    
    def is_published(self) -> bool:
        """Check if post is published."""
        return self.status == PostStatus.PUBLISHED


class Comment(models.Model):
    # Comment representa um comentário feito em um post.

    # ForeignKey para Post: um post pode ter VÁRIOS comentários,
    # mas cada comentário pertence a UM post.
    # on_delete=CASCADE: se o post for deletado, seus comentários também são.
    # related_name='comments': acesso via post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # ForeignKey para User: identificamos quem escreveu o comentário.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)  # comentários passam por moderação antes de aparecer

    class Meta:
        ordering = ['-created_on']  # comentários mais recentes primeiro

    def __str__(self):
        return f'Comentário de {self.author.username} em {self.post.title}'
