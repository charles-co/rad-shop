from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from billing.models import BillingProfile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)