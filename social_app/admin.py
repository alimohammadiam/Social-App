from django.contrib import admin
from .models import User, Post, Comments
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': [
                'date_of_birth', 'bio', 'photo', 'job', 'phone',
            ],
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'update']
    ordering = ['-created']
    search_fields = ['description']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created', 'update']
    search_fields = ['name', 'body']
    list_editable = ['active']
