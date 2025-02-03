from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone']
    fieldsets = [
        ('Additional Information', {
            'fields': [
                'date_of_birth', 'bio', 'photo', 'job', 'phone',
            ],
        }),
    ]
