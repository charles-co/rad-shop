from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from billing.models import BillingProfile
from orders.models import Order
from rad.utils import unique_order_id_generator

@receiver(pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    if instance.shipping_address:
        instance.shipping_address_final = instance.shipping_address.get_address()
        if instance.shipping_address.state.lower() != "lagos":
                instance.shipping_total = 1500
        else:
            instance.shipping_total = 1000
