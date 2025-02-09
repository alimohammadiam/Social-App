from django.contrib import admin
from .models import User, Post
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
