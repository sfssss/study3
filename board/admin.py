from django.contrib import admin

# Register your models here.
from .models import Post

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'created_at')

admin.site.register(Post, BoardAdmin)