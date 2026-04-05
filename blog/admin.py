from django.contrib import admin
from .models import Post, Category, Tag, Comment


class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0
	fields = ('author', 'content', 'is_approved', 'created_on')
	readonly_fields = ('created_on',)
	show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'status', 'created_on', 'updated_on')
	list_filter = ('status', 'created_on', 'updated_on', 'categories', 'tags', 'author')
	search_fields = ('title', 'slug', 'content', 'author__username')
	prepopulated_fields = {'slug': ('title',)}
	filter_horizontal = ('categories', 'tags')
	date_hierarchy = 'created_on'
	ordering = ('-created_on',)
	inlines = [CommentInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_on')
	search_fields = ('name', 'description')
	ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('post', 'author', 'is_approved', 'created_on', 'updated_on')
	list_filter = ('is_approved', 'created_on', 'updated_on', 'author')
	search_fields = ('content', 'author__username', 'post__title')
	actions = ('approve_comments',)
	ordering = ('-created_on',)

	@admin.action(description='Mark selected comments as approved')
	def approve_comments(self, request, queryset):
		queryset.update(is_approved=True)
