from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'gender', 'description')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher')

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Blog, BlogAdmin)
    
# Register your models here.
