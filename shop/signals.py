from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from rad.utils import unique_slug_generator
from shop.models import Product, Trouser, Wavecap

@receiver(pre_save, sender=Trouser)
def trouser_pre_save_receiver(sender, instance, **kwargs):
        instance.slug = unique_slug_generator(instance)

@receiver(post_save, sender=Trouser)
def trouser_post_save_receiver(sender, instance, created, *args, **kwargs):
        if created:
                product = Product.objects.create(item=instance)

@receiver(pre_save, sender=Wavecap)
def wavecap_pre_save_receiver(sender, instance, **kwargs):
        instance.slug = unique_slug_generator(instance)

@receiver(post_save, sender=Wavecap)
def wavecap_post_save_receiver(sender, instance, created, *args, **kwargs):
        if created:
                Product.objects.create(item=instance)