import factory
from faker import Faker
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment
from django.utils.text import slugify


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory para criar usuários de teste"""
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    @classmethod
    def create(cls, **kwargs):
        """Sobrescrever create para adicionar password"""
        obj = super().create(**kwargs)
        obj.set_password('testpass123')
        obj.save()
        return obj


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory para criar categorias de teste"""
    class Meta:
        model = Category
    
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=200)


class TagFactory(factory.django.DjangoModelFactory):
    """Factory para criar tags de teste"""
    class Meta:
        model = Tag
    
    name = factory.Faker('word')


class PostFactory(factory.django.DjangoModelFactory):
    """Factory para criar posts de teste"""
    class Meta:
        model = Post
    
    title = factory.Faker('sentence', nb_words=6)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('text', max_nb_chars=1000)
    status = 1  # Publicado
    
    @factory.post_generation
    def categories(obj, create, extracted, **kwargs):
        """Adicionar categorias após criação"""
        if not create:
            return
        
        if extracted:
            for category in extracted:
                obj.categories.add(category)
        else:
            # Criar 1-2 categorias aleatórias
            for _ in range(fake.random_int(min=1, max=2)):
                obj.categories.add(CategoryFactory())
    
    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Adicionar tags após criação"""
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            # Criar 1-3 tags aleatórias
            for _ in range(fake.random_int(min=1, max=3)):
                obj.tags.add(TagFactory())


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory para criar comentários de teste"""
    class Meta:
        model = Comment
    
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence', nb_words=10)
    is_approved = factory.Faker('boolean')
