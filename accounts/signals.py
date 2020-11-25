from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.dispatch import receiver

from accounts.models import EmailActivation
from accounts.tasks import EmailVerification

User = settings.AUTH_USER_MODEL
use_celery = getattr(settings, "PYTHON_ANYWHERE", False)
@receiver(post_save, sender=User)
def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        if not use_celery:
            EmailVerification.delay(obj.id)
        else:
            obj.send_activation()