from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post, Category, Tag
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Criar um post com categorias e tags'

    def handle(self, *args, **options):
        try:
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
                ''',
                status=1
            )
            
            # Adicionar categorias e tags
            post.categories.add(django_category, python_category)
            post.tags.add(tag_orm, tag_database, tag_tutorial)
            
            self.stdout.write(self.style.SUCCESS('✅ Post criado com sucesso!'))
            self.stdout.write(f'Título: {post.title}')
            self.stdout.write(f'Categorias: {", ".join([c.name for c in post.categories.all()])}')
            self.stdout.write(f'Tags: {", ".join([t.name for t in post.tags.all()])}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Usuário digui não encontrado'))
