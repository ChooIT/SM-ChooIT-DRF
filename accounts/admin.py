from django.contrib import admin
from accounts.models import User, UserTag, Tag, Nickname, NicknameArchive


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'type', 'is_active', 'gender']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_code', 'tag_text']


@admin.register(UserTag)
class UserTagAdmin(admin.ModelAdmin):
    list_display = ['user', 'tag', 'created_at']


@admin.register(Nickname)
class NicknameAdmin(admin.ModelAdmin):
    list_display = ['part', 'content', 'emoji']


@admin.register(NicknameArchive)
class NicknameArchiveAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'count']
