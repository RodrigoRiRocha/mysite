# factories.py — define fábricas para criar objetos de teste automaticamente.
# Usa a biblioteca factory_boy + Faker para gerar dados realistas e aleatórios.
# Vantagem: os testes não precisam criar manualmente cada campo do objeto.

import factory
from faker import Faker
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment, PostStatus
from django.utils.text import slugify


fake = Faker()  # instância do Faker para gerar dados aleatórios (nomes, emails, textos, etc.)


class UserFactory(factory.django.DjangoModelFactory):
    # DjangoModelFactory sabe como salvar o objeto no banco de dados de teste.
    class Meta:
        model = User  # qual model esta factory cria

    # factory.Faker('user_name') gera um username aleatório a cada uso
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @classmethod
    def create(cls, **kwargs):
        # Sobrescrevemos create() para definir uma senha conhecida nos testes.
        # set_password() hasheia a senha antes de salvar (nunca salva em texto puro).
        obj = super().create(**kwargs)
        obj.set_password('testpass123')
        obj.save()
        return obj


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')                          # palavra aleatória como nome
    description = factory.Faker('text', max_nb_chars=200)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    # Use sequence to ensure unique tag names
    name = factory.Sequence(lambda n: f'{fake.word()}-{n}')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    title = factory.Faker('sentence', nb_words=6)                # título com 6 palavras aleatórias
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title)) # gera o slug a partir do título
    author = factory.SubFactory(UserFactory)                     # cria um User automaticamente se não for passado
    content = factory.Faker('text', max_nb_chars=1000)
    status = PostStatus.PUBLISHED  # publicado por padrão nos testes

    @factory.post_generation
    def categories(obj, create, extracted, **kwargs):
        # post_generation é executado APÓS o objeto ser salvo no banco.
        # 'extracted' contém o valor passado explicitamente: PostFactory(categories=[cat1, cat2])
        # Se nada for passado, cria 1 ou 2 categorias aleatórias automaticamente.
        if not create:
            return
        if extracted:
            for category in extracted:
                obj.categories.add(category)
        else:
            for _ in range(fake.random_int(min=1, max=2)):
                obj.categories.add(CategoryFactory())

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        # Mesmo padrão das categorias: usa tags passadas ou cria 1 a 3 aleatórias.
        if not create:
            return
        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            for _ in range(fake.random_int(min=1, max=3)):
                obj.tags.add(TagFactory())


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)    # cria um Post automaticamente se não for passado
    author = factory.SubFactory(UserFactory)  # cria um User automaticamente se não for passado
    content = factory.Faker('sentence', nb_words=10)
    is_approved = factory.Faker('boolean')    # aprovado ou não, aleatoriamente
