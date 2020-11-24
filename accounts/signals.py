from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import EmailActivation
from accounts.tasks import EmailVerification

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        EmailVerification.delay(obj.id)