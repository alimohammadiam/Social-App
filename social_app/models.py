from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(blank=True, null=True, verbose_name='بایو')
    photo = models.ImageField(upload_to='account_images/', blank=True, null=True, verbose_name='عکس پروفایل')
    job = models.CharField(max_length=250, blank=True, null=True, verbose_name='شغل')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post', verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.author.first_name

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name='متن')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name}: {self.post}'















