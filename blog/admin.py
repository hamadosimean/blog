from django.contrib import admin
from .models import Post, Comment


# Register your models here.
admin.site.site_header = "Fatiham Blog"
admin.site.site_title = "Fatiham Blog"
admin.site.index_title = "Welcome to Fatiham Blog"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "body", "post", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "author", "publish", "status")
    list_filter = ("status", "title", "author")
    search_fields = ("author", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
