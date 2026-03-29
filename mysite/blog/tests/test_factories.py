import pytest
from blog.tests.factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory


@pytest.mark.django_db
class TestFactoriesIntegration:
    """Testes para validar as factories e sua integração"""
    
    def test_user_factory_creates_valid_user(self):
        """Testar se UserFactory cria um usuário válido"""
        user = UserFactory()
        assert user.id is not None
        assert user.username is not None
        assert user.email is not None
        assert user.check_password('testpass123')
    
    def test_user_factory_with_custom_username(self):
        """Testar UserFactory com username customizado"""
        user = UserFactory(username='customuser')
        assert user.username == 'customuser'
    
    def test_category_factory_creates_valid_category(self):
        """Testar se CategoryFactory cria uma categoria válida"""
        category = CategoryFactory()
        assert category.id is not None
        assert category.name is not None
        assert category.description is not None
    
    def test_tag_factory_creates_valid_tag(self):
        """Testar se TagFactory cria uma tag válida"""
        tag = TagFactory()
        assert tag.id is not None
        assert tag.name is not None
    
    def test_post_factory_creates_valid_post(self):
        """Testar se PostFactory cria um post válido com author e categorias"""
        post = PostFactory()
        assert post.id is not None
        assert post.title is not None
        assert post.slug is not None
        assert post.author is not None
        assert post.content is not None
        assert post.status == 1
        assert post.categories.count() > 0
        assert post.tags.count() > 0
    
    def test_post_factory_with_specific_user(self):
        """Testar PostFactory com usuário específico"""
        user = UserFactory(username='author123')
        post = PostFactory(author=user)
        assert post.author == user
        assert post.author.username == 'author123'
    
    def test_post_factory_with_specific_categories(self):
        """Testar PostFactory com categorias específicas"""
        category1 = CategoryFactory(name='Django')
        category2 = CategoryFactory(name='Python')
        post = PostFactory(categories=[category1, category2])
        assert post.categories.count() == 2
        assert category1 in post.categories.all()
        assert category2 in post.categories.all()
    
    def test_post_factory_with_specific_tags(self):
        """Testar PostFactory com tags específicas"""
        tag1 = TagFactory(name='ORM')
        tag2 = TagFactory(name='Database')
        post = PostFactory(tags=[tag1, tag2])
        assert post.tags.count() == 2
        assert tag1 in post.tags.all()
        assert tag2 in post.tags.all()
    
    def test_comment_factory_creates_valid_comment(self):
        """Testar se CommentFactory cria um comentário válido"""
        comment = CommentFactory()
        assert comment.id is not None
        assert comment.post is not None
        assert comment.author is not None
        assert comment.content is not None
    
    def test_comment_factory_with_specific_post(self):
        """Testar CommentFactory com post específico"""
        post = PostFactory()
        comment = CommentFactory(post=post)
        assert comment.post == post
    
    def test_bulk_user_creation(self):
        """Testar criação em massa de usuários"""
        users = UserFactory.create_batch(5)
        assert len(users) == 5
        for user in users:
            assert user.id is not None
            assert user.username is not None
    
    def test_bulk_post_creation_with_relationships(self):
        """Testar criação em massa de posts com relacionamentos"""
        posts = PostFactory.create_batch(3)
        assert len(posts) == 3
        for post in posts:
            assert post.id is not None
            assert post.author is not None
            assert post.categories.count() > 0
            assert post.tags.count() > 0
    
    def test_bulk_comment_creation(self):
        """Testar criação em massa de comentários"""
        post = PostFactory()
        comments = CommentFactory.create_batch(5, post=post)
        assert len(comments) == 5
        assert post.comments.count() == 5
    
    def test_factories_generate_realistic_data_with_faker(self):
        """Testar se as factories geram dados realistas com Faker"""
        user = UserFactory()
        assert '@' in user.email  # Email deve ter @
        assert len(user.username) > 0
        
        post = PostFactory()
        assert len(post.title) > 0
        assert len(post.slug) > 0
        assert len(post.content) > 100  # Conteúdo deve ter texto suficiente
        
        comment = CommentFactory()
        assert len(comment.content) > 0


@pytest.mark.django_db
class TestComplexScenariosWithFactories:
    """Testes de cenários complexos usando factories"""
    
    def test_create_blog_with_multiple_posts_and_comments(self):
        """Testar criação de um blog com múltiplos posts e comentários"""
        # Criar um autor
        author = UserFactory(username='blogger')
        
        # Criar categorias
        categoria_tech = CategoryFactory(name='Tecnologia')
        categoria_python = CategoryFactory(name='Python')
        
        # Criar posts
        post1 = PostFactory(author=author, categories=[categoria_tech, categoria_python])
        post2 = PostFactory(author=author, categories=[categoria_tech])
        
        # Criar comentários
        CommentFactory.create_batch(3, post=post1)
        CommentFactory.create_batch(2, post=post2)
        
        # Validações
        assert author.blog_posts.count() == 2
        assert post1.comments.count() == 3
        assert post2.comments.count() == 2
        assert categoria_tech.posts.count() == 2
        assert categoria_python.posts.count() == 1
    
    def test_create_multiple_authors_with_posts(self):
        """Testar criação de múltiplos autores com seus posts"""
        authors = UserFactory.create_batch(3)
        
        for author in authors:
            posts = PostFactory.create_batch(2, author=author)
            assert author.blog_posts.count() == 2
        
        assert len(authors) == 3
