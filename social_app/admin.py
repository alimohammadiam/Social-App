from django.contrib import admin
from .models import User, Post, Comments, Image, Contact
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comments
    extra = 0


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


def make_deactivation(modeladmin, request, queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request, f'{result} Posts were deactivation')


make_deactivation.short_description = 'رد پست'


def make_activation(modeladmin, request, queryset):
    result = queryset.update(active=True)
    modeladmin.message_user(request, f'{result} Posts were activate')


make_activation.short_description = "تایید پست"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'update', 'description']
    ordering = ['-created']
    search_fields = ['description']
    inlines = [ImageInline, CommentInline]
    actions = [make_deactivation, make_activation]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created', 'update']
    search_fields = ['name', 'body']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created']


admin.site.register(Contact)
