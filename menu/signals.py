from django.db.models.signals import pre_save
from django.dispatch import receiver

from rad.utils import unique_slug_generator
from menu.models import Menu

@receiver(pre_save, sender=Menu)
def menu_pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, None, "menu")