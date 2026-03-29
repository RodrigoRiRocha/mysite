import pytest
from django.utils.text import slugify
from blog.models import Post, Category, Tag, Comment
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPostModel:
    """Testes para o modelo Post"""
    
    def test_post_creation(self, user):
        """Testar se um post pode ser criado"""
        post = Post.objects.create(
            title='Test Post',
            slug=slugify('Test Post'),
            author=user,
            content='Test content',
            status=1
        )
        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.author == user
        assert post.status == 1
    
    def test_post_string_representation(self, post):
        """Testar a representação em string do post"""
        assert str(post) == post.title
    
    def test_post_slug_unique(self, user):
        """Testar se o slug é único"""
        Post.objects.create(
            title='Unique Post',
            slug='unique-post',
            author=user,
            content='Content',
            status=1
        )
        
        # Tentar criar outro post com o mesmo slug deve falhar
        with pytest.raises(Exception):
            Post.objects.create(
                title='Another Post',
                slug='unique-post',
                author=user,
                content='Content',
                status=1
            )
    
    def test_post_ordering(self, user):
        """Testar se os posts são ordenados por data de criação (mais recentes primeiro)"""
        post1 = Post.objects.create(
            title='Post 1',
            slug='post-1',
            author=user,
            content='Content 1',
            status=1
        )
        post2 = Post.objects.create(
            title='Post 2',
            slug='post-2',
            author=user,
            content='Content 2',
            status=1
        )
        
        posts = list(Post.objects.all())
        # O post mais recente deve estar primeiro
        assert posts[0].id == post2.id
        assert posts[1].id == post1.id
    
    def test_post_can_have_multiple_categories(self, user):
        """Testar se um post pode ter múltiplas categorias"""
        # Criar post sem categorias pre-definidas
        post = Post.objects.create(
            title='Test Post',
            slug='test-post-categories',
            author=user,
            content='Test content',
            status=1
        )
        
        category = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')
        
        post.categories.add(category)
        post.categories.add(category2)
        
        assert post.categories.count() == 2
        assert category in post.categories.all()
        assert category2 in post.categories.all()
    
    def test_post_can_have_multiple_tags(self, user):
        """Testar se um post pode ter múltiplas tags"""
        # Criar post sem tags pre-definidas
        post = Post.objects.create(
            title='Test Post Tags',
            slug='test-post-tags',
            author=user,
            content='Test content',
            status=1
        )
        
        tag1 = Tag.objects.create(name='Django')
        tag2 = Tag.objects.create(name='Python')
        tag3 = Tag.objects.create(name='Testing')
        
        post.tags.add(tag1, tag2, tag3)
        
        assert post.tags.count() == 3
        assert tag1 in post.tags.all()
        assert tag2 in post.tags.all()
        assert tag3 in post.tags.all()


@pytest.mark.django_db
class TestCategoryModel:
    """Testes para o modelo Category"""
    
    def test_category_creation(self):
        """Testar se uma categoria pode ser criada"""
        category = Category.objects.create(
            name='Django',
            description='Posts sobre Django'
        )
        assert category.id is not None
        assert category.name == 'Django'
    
    def test_category_string_representation(self):
        """Testar a representação em string da categoria"""
        category = Category.objects.create(name='Django')
        assert str(category) == 'Django'
    
    def test_category_related_posts(self, user):
        """Testar se uma categoria pode ter múltiplos posts relacionados"""
        category = Category.objects.create(name='Django')
        
        post1 = Post.objects.create(
            title='Post 1',
            slug='post-1',
            author=user,
            content='Content 1',
            status=1
        )
        post2 = Post.objects.create(
            title='Post 2',
            slug='post-2',
            author=user,
            content='Content 2',
            status=1
        )
        
        post1.categories.add(category)
        post2.categories.add(category)
        
        assert category.posts.count() == 2
        assert post1 in category.posts.all()
        assert post2 in category.posts.all()


@pytest.mark.django_db
class TestTagModel:
    """Testes para o modelo Tag"""
    
    def test_tag_creation(self):
        """Testar se uma tag pode ser criada"""
        tag = Tag.objects.create(name='ORM')
        assert tag.id is not None
        assert tag.name == 'ORM'
    
    def test_tag_string_representation(self):
        """Testar a representação em string da tag"""
        tag = Tag.objects.create(name='Django')
        assert str(tag) == 'Django'
    
    def test_tag_unique_name(self):
        """Testar se o nome da tag é único"""
        Tag.objects.create(name='Django')
        
        with pytest.raises(Exception):
            Tag.objects.create(name='Django')


@pytest.mark.django_db
class TestCommentModel:
    """Testes para o modelo Comment"""
    
    def test_comment_creation(self, post, user):
        """Testar se um comentário pode ser criado"""
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Great post!',
            is_approved=False
        )
        assert comment.id is not None
        assert comment.post == post
        assert comment.author == user
        assert comment.is_approved is False
    
    def test_comment_string_representation(self, comment):
        """Testar a representação em string do comentário"""
        expected = f'Comentário de {comment.author.username} em {comment.post.title}'
        assert str(comment) == expected
    
    def test_comment_approval(self, comment):
        """Testar se um comentário pode ser aprovado"""
        assert comment.is_approved is True
        
        comment.is_approved = False
        comment.save()
        
        comment.refresh_from_db()
        assert comment.is_approved is False
    
    def test_post_related_comments(self, post, user):
        """Testar se um post pode ter múltiplos comentários"""
        comment1 = Comment.objects.create(
            post=post,
            author=user,
            content='Comment 1',
            is_approved=True
        )
        comment2 = Comment.objects.create(
            post=post,
            author=user,
            content='Comment 2',
            is_approved=True
        )
        
        assert post.comments.count() == 2
        assert comment1 in post.comments.all()
        assert comment2 in post.comments.all()
    
    def test_comment_cascade_delete(self, post, user):
        """Testar se comentários são deletados quando um post é deletado"""
        Comment.objects.create(
            post=post,
            author=user,
            content='Comment 1',
            is_approved=True
        )
        Comment.objects.create(
            post=post,
            author=user,
            content='Comment 2',
            is_approved=True
        )
        
        assert Comment.objects.count() == 2
        
        post.delete()
        
        assert Comment.objects.count() == 0
    
    def test_comment_ordering(self, post, user):
        """Testar se os comentários são ordenados por data de criação (mais recentes primeiro)"""
        comment1 = Comment.objects.create(
            post=post,
            author=user,
            content='Comment 1',
            is_approved=True
        )
        comment2 = Comment.objects.create(
            post=post,
            author=user,
            content='Comment 2',
            is_approved=True
        )
        
        comments = list(post.comments.all())
        assert comments[0].id == comment2.id
        assert comments[1].id == comment1.id
