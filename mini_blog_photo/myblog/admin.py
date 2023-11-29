from django.contrib import admin

from myblog.models import Comment, Photo, Like, User


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'text', 'create_at', 'user')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('is_like', 'user', 'photo')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'img')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
