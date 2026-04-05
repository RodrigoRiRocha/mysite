import pytest
from django.utils.text import slugify
from django.db import IntegrityError
from blog.models import Post, Category, Tag, Comment, PostStatus
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPostModel:

    def test_post_creation(self, user):
        post = Post.objects.create(
            title='Test Post',
            slug=slugify('Test Post'),
            author=user,
            content='Test content',
            status=PostStatus.PUBLISHED
        )
        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.author == user
        assert post.status == PostStatus.PUBLISHED
    
    def test_post_is_published_helper(self, user):
        draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=user,
            content='Content',
            status=PostStatus.DRAFT
        )
        published_post = Post.objects.create(
            title='Published Post',
            slug='published-post',
            author=user,
            content='Content',
            status=PostStatus.PUBLISHED
        )
        assert not draft_post.is_published()
        assert published_post.is_published()

    def test_post_string_representation(self, post):
        assert str(post) == post.title

    def test_post_slug_unique(self, user):
        Post.objects.create(title='Unique Post', slug='unique-post', author=user, content='Content', status=PostStatus.PUBLISHED)
        with pytest.raises(IntegrityError):
            Post.objects.create(title='Another Post', slug='unique-post', author=user, content='Content', status=PostStatus.PUBLISHED)

    def test_post_ordering(self, user):
        post1 = Post.objects.create(title='Post 1', slug='post-1', author=user, content='Content 1', status=PostStatus.PUBLISHED)
        post2 = Post.objects.create(title='Post 2', slug='post-2', author=user, content='Content 2', status=PostStatus.PUBLISHED)
        posts = list(Post.objects.all())
        assert posts[0].id == post2.id
        assert posts[1].id == post1.id

    def test_post_can_have_multiple_categories(self, user):
        post = Post.objects.create(title='Test Post', slug='test-post-categories', author=user, content='Test content', status=PostStatus.PUBLISHED)
        cat1 = Category.objects.create(name='Category 1')
        cat2 = Category.objects.create(name='Category 2')
        post.categories.add(cat1, cat2)
        assert post.categories.count() == 2

    def test_post_can_have_multiple_tags(self, user):
        post = Post.objects.create(title='Test Post Tags', slug='test-post-tags', author=user, content='Test content', status=PostStatus.PUBLISHED)
        tag1 = Tag.objects.create(name='Django')
        tag2 = Tag.objects.create(name='Python')
        tag3 = Tag.objects.create(name='Testing')
        post.tags.add(tag1, tag2, tag3)
        assert post.tags.count() == 3


@pytest.mark.django_db
class TestCategoryModel:

    def test_category_creation(self):
        category = Category.objects.create(name='Django', description='Posts sobre Django')
        assert category.id is not None
        assert category.name == 'Django'

    def test_category_string_representation(self):
        category = Category.objects.create(name='Django')
        assert str(category) == 'Django'

    def test_category_related_posts(self, user):
        category = Category.objects.create(name='Django')
        post1 = Post.objects.create(title='Post 1', slug='post-1', author=user, content='Content 1', status=PostStatus.PUBLISHED)
        post2 = Post.objects.create(title='Post 2', slug='post-2', author=user, content='Content 2', status=PostStatus.PUBLISHED)
        post1.categories.add(category)
        post2.categories.add(category)
        assert category.posts.count() == 2


@pytest.mark.django_db
class TestTagModel:

    def test_tag_creation(self):
        tag = Tag.objects.create(name='ORM')
        assert tag.id is not None
        assert tag.name == 'ORM'

    def test_tag_string_representation(self):
        tag = Tag.objects.create(name='Django')
        assert str(tag) == 'Django'

    def test_tag_unique_name(self):
        Tag.objects.create(name='Django')
        with pytest.raises(IntegrityError):
            Tag.objects.create(name='Django')


@pytest.mark.django_db
class TestCommentModel:

    def test_comment_creation(self, post, user):
        comment = Comment.objects.create(post=post, author=user, content='Great post!', is_approved=False)
        assert comment.id is not None
        assert comment.post == post
        assert comment.author == user
        assert comment.is_approved is False

    def test_comment_string_representation(self, comment):
        expected = f'Comentário de {comment.author.username} em {comment.post.title}'
        assert str(comment) == expected

    def test_comment_approval(self, comment):
        assert comment.is_approved is True
        comment.is_approved = False
        comment.save()
        comment.refresh_from_db()
        assert comment.is_approved is False

    def test_post_related_comments(self, post, user):
        comment1 = Comment.objects.create(post=post, author=user, content='Comment 1', is_approved=True)
        comment2 = Comment.objects.create(post=post, author=user, content='Comment 2', is_approved=True)
        assert post.comments.count() == 2
        assert comment1 in post.comments.all()
        assert comment2 in post.comments.all()

    def test_comment_cascade_delete(self, post, user):
        Comment.objects.create(post=post, author=user, content='Comment 1', is_approved=True)
        Comment.objects.create(post=post, author=user, content='Comment 2', is_approved=True)
        assert Comment.objects.count() == 2
        post.delete()
        assert Comment.objects.count() == 0

    def test_comment_ordering(self, post, user):
        comment1 = Comment.objects.create(post=post, author=user, content='Comment 1', is_approved=True)
        comment2 = Comment.objects.create(post=post, author=user, content='Comment 2', is_approved=True)
        comments = list(post.comments.all())
        assert comments[0].id == comment2.id
        assert comments[1].id == comment1.id
