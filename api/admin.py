from django.contrib import admin
from .models import Tag, Blog, ContentImage


class ContentImageInline(admin.TabularInline):
    model = ContentImage


class BlogAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]


admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
