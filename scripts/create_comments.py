import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.config.settings')
django.setup()

from blog.models import Post, Comment
from django.contrib.auth.models import User

# Buscar usuário
user = User.objects.get(username='digui')

# Buscar o primeiro post
post = Post.objects.first()

# Criar comentários
comment1 = Comment.objects.create(
    post=post,
    author=user,
    content='Excelente post! Muito claro e didático.',
    is_approved=True
)

comment2 = Comment.objects.create(
    post=post,
    author=user,
    content='Gostaria de mais exemplos práticos.',
    is_approved=True
)

print(f'✅ Comentários criados com sucesso!')
print(f'\nPost: {post.title}')
print(f'Comentários do post:')
for comment in post.comments.all():
    print(f'  - {comment.author.username}: "{comment.content[:50]}..."')
    print(f'    Status: {"Aprovado ✓" if comment.is_approved else "Pendente ⏳"}')
