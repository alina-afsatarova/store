from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from .models import CustomGroup, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username',)


admin.site.unregister(Group)


@admin.register(CustomGroup)
class CustomGroupAdmin(GroupAdmin):
    pass
