from django.core.management.base import BaseCommand
from blog.models import Post, Comment
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Criar comentários de exemplo nos posts'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='digui')
            post = Post.objects.first()
            
            if not post:
                self.stdout.write(self.style.ERROR('❌ Nenhum post encontrado'))
                return
            
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
            
            self.stdout.write(self.style.SUCCESS('✅ Comentários criados com sucesso!'))
            self.stdout.write(f'Post: {post.title}')
            self.stdout.write(f'Comentários criados: 2')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Usuário digui não encontrado'))
