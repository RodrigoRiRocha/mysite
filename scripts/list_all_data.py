import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.config.settings')
django.setup()

from blog.models import Post, Category, Comment
from django.contrib.auth.models import User

print('=' * 60)
print('DADOS CRIADOS - CONSULTAS COMPLETAS')
print('=' * 60)

# Buscar usuário
user = User.objects.get(username='digui')
print(f'\n👤 USUÁRIO: {user.username}')
print(f'   Email: {user.email}')
print(f'   Total de posts: {user.blog_posts.count()}')
print(f'   Total de comentários: {user.comments.count()}')

# Listar todos os posts
print(f'\n📝 POSTS DO USUÁRIO:')
for post in user.blog_posts.all():
    print(f'\n   Título: {post.title}')
    print(f'   Status: {"Publicado ✓" if post.status == 1 else "Rascunho"}')
    print(f'   Categorias: {", ".join([c.name for c in post.categories.all()]) or "Sem categorias"}')
    print(f'   Tags: {", ".join([t.name for t in post.tags.all()]) or "Sem tags"}')
    print(f'   Comentários: {post.comments.count()}')
    for i, comment in enumerate(post.comments.all(), 1):
        print(f'      {i}. "{comment.content}"')

# Consultar por categoria
print(f'\n📂 POSTS POR CATEGORIA:')
for category in Category.objects.all():
    print(f'\n   {category.name} ({category.posts.count()} posts)')
    for post in category.posts.all():
        print(f'      - {post.title}')
