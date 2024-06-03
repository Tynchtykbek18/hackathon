from django.contrib import admin
from apps.user.models import User, Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'department', 'role')
    list_display_links = ('id', 'email')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'department', 'role')
    list_display_links = ('id', 'email')
