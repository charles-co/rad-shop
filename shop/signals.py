from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from rad.utils import unique_slug_generator
from shop.models import Product, Trouser, Wavecap

@receiver(post_save, sender=Trouser)
def trouser_post_save_receiver(sender, instance, created, *args, **kwargs):
        if created:
                instance.slug = unique_slug_generator(instance)
                Product.objects.create(item=instance, name=instance.name, 
                                        price=instance.variants.first().price, available=instance.available, 
                                        is_back=instance.is_back, is_discounted=instance.is_discounted,
                                        is_bestseller=instance.is_bestseller, is_featured=instance.is_featured)

@receiver(post_save, sender=Wavecap)
def wavecap_post_save_receiver(sender, instance, created, *args, **kwargs):
        if created:
                instance.slug = unique_slug_generator(instance)
                Product.objects.create(item=instance, name=instance.name, 
                                        price=instance.variants.first().price, available=instance.available, 
                                        is_back=instance.is_back, is_discounted=instance.is_discounted,
                                        is_bestseller=instance.is_bestseller, is_featured=instance.is_featured)
