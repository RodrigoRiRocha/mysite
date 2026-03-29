import pytest
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment
from blog.tests.factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory
from django.utils.text import slugify


@pytest.fixture
def user():
    """Criar um usuário de teste usando factory"""
    return UserFactory(username='testuser', email='test@example.com')


@pytest.fixture
def category():
    """Criar uma categoria de teste usando factory"""
    return CategoryFactory(name='Django', description='Posts sobre Django')


@pytest.fixture
def tag():
    """Criar uma tag de teste usando factory"""
    return TagFactory(name='ORM')


@pytest.fixture
def post(user, category):
    """Criar um post de teste usando factory"""
    post = PostFactory(author=user)
    post.categories.add(category)
    return post


@pytest.fixture
def comment(post, user):
    """Criar um comentário de teste usando factory"""
    return CommentFactory(post=post, author=user, is_approved=True)
