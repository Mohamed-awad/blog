from django.contrib import admin
from .models import Post, Like


class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'author', 'status', 'created', 'image')
  list_filter = ('status', 'created', 'publish', 'author')
  search_fields = ('title', 'author')
  prepopulated_fields = {'slug': ('title',)}
  date_hierarchy = 'publish'
  ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
