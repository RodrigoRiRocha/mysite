from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Criar um novo post de exemplo'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='digui')
            
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
                status=1
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Post criado com sucesso!'))
            self.stdout.write(f'ID: {post.id}')
            self.stdout.write(f'Título: {post.title}')
            self.stdout.write(f'Slug: {post.slug}')
            self.stdout.write(f'Autor: {post.author.username}')
            self.stdout.write(f'Status: Publicado')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Usuário digui não encontrado'))
