# conftest.py — arquivo especial do pytest lido automaticamente antes dos testes.
# Define fixtures: objetos reutilizáveis que os testes podem receber como parâmetro.
# Quando um teste declara 'def test_algo(user)', o pytest injeta a fixture 'user' automaticamente.

import pytest
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment
from blog.tests.factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory
from django.utils.text import slugify


@pytest.fixture
def user():
    # Cria e retorna um usuário de teste com username fixo.
    # Qualquer teste que receber 'user' como parâmetro vai usar este objeto.
    return UserFactory(username='testuser', email='test@example.com')


@pytest.fixture
def category():
    # Categoria de teste reutilizável entre os testes.
    return CategoryFactory(name='Django', description='Posts sobre Django')


@pytest.fixture
def tag():
    return TagFactory(name='ORM')


@pytest.fixture
def post(user, category):
    # Depende das fixtures 'user' e 'category' — o pytest as injeta automaticamente.
    # Cria um post publicado e adiciona a categoria a ele.
    post = PostFactory(author=user)
    post.categories.add(category)
    return post


@pytest.fixture
def comment(post, user):
    # Cria um comentário já aprovado ligado ao post e ao usuário acima.
    return CommentFactory(post=post, author=user, is_approved=True)
