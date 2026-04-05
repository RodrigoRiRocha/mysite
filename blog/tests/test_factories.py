import pytest
from blog.tests.factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory
from blog.models import PostStatus


@pytest.mark.django_db
class TestFactoriesIntegration:

    def test_user_factory_creates_valid_user(self):
        user = UserFactory()
        assert user.id is not None
        assert user.username is not None
        assert user.check_password('testpass123')

    def test_category_factory_creates_valid_category(self):
        category = CategoryFactory()
        assert category.id is not None
        assert category.name is not None

    def test_tag_factory_creates_valid_tag(self):
        tag = TagFactory()
        assert tag.id is not None
        assert tag.name is not None

    def test_post_factory_creates_valid_post(self):
        post = PostFactory()
        assert post.id is not None
        assert post.author is not None
        assert post.status == PostStatus.PUBLISHED
        assert post.categories.count() > 0
        assert post.tags.count() > 0

    def test_post_factory_with_specific_user(self):
        user = UserFactory(username='author123')
        post = PostFactory(author=user)
        assert post.author.username == 'author123'

    def test_post_factory_with_specific_categories(self):
        cat1 = CategoryFactory(name='Django')
        cat2 = CategoryFactory(name='Python')
        post = PostFactory(categories=[cat1, cat2])
        assert post.categories.count() == 2

    def test_comment_factory_creates_valid_comment(self):
        comment = CommentFactory()
        assert comment.id is not None
        assert comment.post is not None
        assert comment.author is not None

    def test_bulk_post_creation_with_relationships(self):
        posts = PostFactory.create_batch(3)
        assert len(posts) == 3
        for post in posts:
            assert post.categories.count() > 0

    def test_bulk_comment_creation(self):
        post = PostFactory()
        comments = CommentFactory.create_batch(5, post=post)
        assert len(comments) == 5
        assert post.comments.count() == 5


@pytest.mark.django_db
class TestComplexScenarios:

    def test_create_blog_with_multiple_posts_and_comments(self):
        author = UserFactory(username='blogger')
        cat_tech = CategoryFactory(name='Tecnologia')
        cat_python = CategoryFactory(name='Python')
        post1 = PostFactory(author=author, categories=[cat_tech, cat_python])
        post2 = PostFactory(author=author, categories=[cat_tech])
        CommentFactory.create_batch(3, post=post1)
        CommentFactory.create_batch(2, post=post2)
        assert author.blog_posts.count() == 2
        assert post1.comments.count() == 3
        assert post2.comments.count() == 2
        assert cat_tech.posts.count() == 2
        assert cat_python.posts.count() == 1

    def test_create_multiple_authors_with_posts(self):
        authors = UserFactory.create_batch(3)
        for author in authors:
            PostFactory.create_batch(2, author=author)
            assert author.blog_posts.count() == 2
