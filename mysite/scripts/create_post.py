import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.config.settings')
django.setup()

from blog.models import Post, Category
from django.contrib.auth.models import User
from django.utils.text import slugify

# Buscar ou criar usuário
user = User.objects.get(username='digui')

# Criar o novo post
post = Post.objects.create(
    title='Introdução ao Django ORM',
    slug=slugify('Introdução ao Django ORM'),
    author=user,
    content='''
    O Django ORM (Object-Relational Mapping) é uma ferramenta poderosa que permite 
    interagir com o banco de dados usando objetos Python, sem escrever SQL direto.
    
    Vantagens:
    - Não precisa escrever SQL
    - Código mais legível e pythônico
    - Proteção contra SQL Injection
    - Fácil de trabalhar com relacionamentos
    ''',
    status=1  # 1 = Published
)

print(f'✅ Post criado com sucesso!')
print(f'ID: {post.id}')
print(f'Título: {post.title}')
print(f'Slug: {post.slug}')
print(f'Autor: {post.author.username}')
print(f'Data de criação: {post.created_on}')
print(f'Status: {"Publicado" if post.status == 1 else "Rascunho"}')
