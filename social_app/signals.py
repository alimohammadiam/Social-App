from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.likes.through)
def user_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def delete_post_email(sender, instance, **kwargs):
    author = instance.author
    subject = "Your Post has been deleted"
    message = f'Your Post has beeb Deleted (ID: {instance.id})'
    send_mail(subject, message, 'ali0182mohammadi@gmail.com', [author.email], fail_silently=False)

