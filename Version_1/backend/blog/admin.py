from django.contrib import admin

from .models import Post, Comment, Tag


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ['title']}


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
