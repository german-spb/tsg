from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from django_summernote.admin import SummernoteModelAdmin
from .models import Documents, Entry, BlogPost, Comment

admin.site.register(Documents)
# admin.site.register(BlogPost)
# admin.site.register(Comment)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_created')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author', 'text', 'created_at')

# @admin.register(BlogPost)
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('author','title', 'content', 'date_created')
#
#     formfield_overrides = {
#         models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
#     }

class BlogPostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content',)

admin.site.register(BlogPost, BlogPostAdmin)

