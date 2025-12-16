from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from django_summernote.admin import SummernoteModelAdmin
from .models import Documents, Entry, BlogPost, Comment

admin.site.register(Documents)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author', 'text', 'created_at')


class BlogPostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content',)
    list_display = ('author', 'title', 'content', 'date_created')
admin.site.register(BlogPost, BlogPostAdmin)


class EntryAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')
    list_display = ('title', 'content', 'date_created')
admin.site.register(Entry, EntryAdmin)


