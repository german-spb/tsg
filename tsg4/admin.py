from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Documents, Entry

admin.site.register(Documents)
# admin.site.register(Entry)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_created')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }