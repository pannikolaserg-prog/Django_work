from django.contrib import admin
from .models import MyBlog

@admin.register(MyBlog)
class MyBlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published', 'views_count', 'created_at']
    list_filter = ['is_published', 'created_at']
    list_editable = ['is_published', 'views_count']
    search_fields = ['name', 'description']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
