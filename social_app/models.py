import os

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
    likes = models.ManyToManyField(User, related_name='liked_post', blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return f'{self.author.first_name}: {self.description}'

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            if img.image_field:
                storage, path = img.image_field.storage, img.image_field.path
                if os.path.exists(path):
                    storage.delete(path)
            img.delete()
        super().delete(*args, **kwargs)


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


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_field = models.ImageField(upload_to='post_image/')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, path = self.image_field.storage, self.image_field.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'

    def __str__(self):
        return f'{self.title}' if self.title else f'{self.post.author}'


