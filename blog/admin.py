from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'view_count',)
    prepopulated_fields = {'slug': ('name',)}
