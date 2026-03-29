import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.config.settings')
django.setup()

from blog.models import Post, Category, Tag
from django.contrib.auth.models import User
from django.utils.text import slugify

# Buscar usuário
user = User.objects.get(username='digui')

# Criar ou obter categorias
django_category, _ = Category.objects.get_or_create(
    name='Django',
    defaults={'description': 'Posts sobre Django Framework'}
)

python_category, _ = Category.objects.get_or_create(
    name='Python',
    defaults={'description': 'Posts sobre Python'}
)

# Criar ou obter tags
tag_orm, _ = Tag.objects.get_or_create(name='ORM')
tag_database, _ = Tag.objects.get_or_create(name='Database')
tag_tutorial, _ = Tag.objects.get_or_create(name='Tutorial')

# Criar novo post
post = Post.objects.create(
    title='Relacionamentos em Django - ForeignKey vs ManyToMany',
    slug=slugify('Relacionamentos em Django - ForeignKey vs ManyToMany'),
    author=user,
    content='''
    Entender os relacionamentos é fundamental para modelar dados em Django.
    
    ## ForeignKey (Um para Muitos)
    - Um registro a muitos
    - Exemplo: Um autor escreve vários posts
    
    ## ManyToMany (Muitos para Muitos)
    - Muitos registros a muitos
    - Exemplo: Um post tem várias categorias, uma categoria tem vários posts
    
    ## OneToOneField
    - Uma relação um para um
    - Exemplo: Um usuário tem um perfil
    
    Escolha o tipo certo para melhor desempenho!
    ''',
    status=1  # Publicado
)

# Adicionar categorias
post.categories.add(django_category, python_category)

# Adicionar tags
post.tags.add(tag_orm, tag_database, tag_tutorial)

print(f'✅ Post criado com sucesso!')
print(f'Título: {post.title}')
print(f'Categorias: {", ".join([c.name for c in post.categories.all()])}')
print(f'Tags: {", ".join([t.name for t in post.tags.all()])}')
