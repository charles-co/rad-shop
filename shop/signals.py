from django.db.models.signals import pre_save
from django.dispatch import receiver

from rad.utils import unique_slug_generator
from shop.models import Trouser


@receiver(pre_save, sender=Trouser)
def product_pre_save_receiver(sender, instance, **kwargs):
        instance.slug = unique_slug_generator(instance)