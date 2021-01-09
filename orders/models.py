import datetime
import math

from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg, Count, Sum
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils import timezone

from addresses.models import Address
from billing.models import BillingProfile
from rad.utils import unique_order_id_generator
from shop.models import TrouserVariant

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

#     def get_sales_breakdown(self):
#         recent = self.recent().not_refunded()
#         recent_data = recent.totals_data()
#         shipped = recent.not_refunded().by_status(status='shipped')
#         shipped_data = shipped.totals_data()
#         paid = recent.by_status(status='paid')
#         paid_data = paid.totals_data()
#         data = {
#             'recent': recent,
#             'recent_data':recent_data,
#             'shipped': shipped,
#             'shipped_data': shipped_data,
#             'paid': paid,
#             'paid_data': paid_data
#         }
#         return data

#     def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
#         if number_of_weeks > weeks_ago:
#             number_of_weeks = weeks_ago
#         days_ago_start = weeks_ago * 7  # days_ago_start = 49
#         days_ago_end = days_ago_start - (number_of_weeks * 7) #days_ago_end = 49 - 14 = 35
#         start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
#         end_date = timezone.now() - datetime.timedelta(days=days_ago_end) 
#         return self.by_range(start_date, end_date=end_date)

#     def by_range(self, start_date, end_date=None):
#         if end_date is None:
#             return self.filter(updated__gte=start_date)
#         return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

#     def by_date(self):
#         now = timezone.now() - datetime.timedelta(days=9)
#         return self.filter(updated__day__gte=now.day)

#     def totals_data(self):
#         return self.aggregate(Sum("total"), Avg("total"))

#     def by_status(self, status="shipped"):
#         return self.filter(status=status)

#     def not_refunded(self):
#         return self.exclude(status='refunded')

#     def by_request(self, request):
#         billing_profile = BillingProfile.objects.new_or_get(request)
#         return self.filter(billing_profile=billing_profile)

#     def not_created(self):
#         return self.exclude(status='created')
class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)
#     def by_request(self, request):
#         return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, order_id=None):
        created = False
        if order_id is not None:
            qs = self.get_queryset().filter(
                    billing_profile=billing_profile,
                    active=True, 
                    status='created',
                    id=order_id
                )
            if qs.count() == 1:
                obj = qs.first()
            elif qs.count() == 0:
                obj = self.model.objects.create(
                    billing_profile=billing_profile)
                created = True
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile)
            created = True
        return obj



# Random, Unique
class Order(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    order_id            = models.CharField(max_length=120, blank=True) # AB31DE3
    shipping_address    = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, on_delete=models.SET_NULL)
    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('trouservariant','wavecapvariant')})
    object_id           = models.PositiveIntegerField()
    item                = GenericForeignKey('content_type', 'object_id')
    shipping_address_final = models.TextField(blank=True, null=True)
    status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(default=1000.00, max_digits=100, decimal_places=2)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    # def save(self, *args, **kwargs):
    #     if self.shipping_address is not None:
    #         if self.shipping_address.state.lower() != "lagos":
    #             self.shipping_total = 1500
    #     super().save(*args, **kwargs)

    class Meta:
       ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.orders.all())

    # def check_done(self):
    #     shipping_done = False
    #     if self.shipping_address:
    #         shipping_done = True
    #     elif shipping_address_required and not self.shipping_address:
    #         shipping_done = False
    #     else:
    #         shipping_done = True
    #     billing_profile = self.billing_profile
    #     billing_address = self.shipping_address
    #     total   = self.total
    #     if billing_profile and shipping_done and billing_address and total > 0:
    #         return True
    #     return False

    def mark_paid(self):
        if self.status != 'paid':
            self.status = "paid"
            self.save()
            # self.update_purchases()
        return self.status


# def post_save_order(sender, instance, created, *args, **kwargs):
#     #print("running")
#     if created:
#         print("Updating... first")
#         # instance.update_total()


# post_save.connect(post_save_order, sender=Order)



# class ProductPurchaseQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(refunded=False)

#     def by_request(self, request):
#         billing_profile, created = BillingProfile.objects.new_or_get(request)
#         return self.filter(billing_profile=billing_profile)



# class ProductPurchaseManager(models.Manager):
#     def get_queryset(self):
#         return ProductPurchaseQuerySet(self.model, using=self._db)

#     def all(self):
#         return self.get_queryset().active()

#     def by_request(self, request):
#         return self.get_queryset().by_request(request)

#     def products_by_id(self, request):
#         qs = self.by_request(request).digital()
#         ids_ = [x.product.id for x in qs]
#         return ids_

#     def products_by_request(self, request):
#         ids_ = self.products_by_id(request)
#         products_qs = Product.objects.filter(id__in=ids_).distinct()
#         return products_qs



class OrderItem(models.Model):
    order               = models.ForeignKey(Order, related_name="orders", on_delete=models.CASCADE)
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name="billing_profiles")
    price               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    quantity               = models.PositiveIntegerField(default=1)
    size               = models.CharField(max_length=2,default="32")
    refunded            = models.BooleanField(default=False)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    # objects = ProductPurchaseManager()

    def __str__(self):
        return self.trouser.trouser.name

    def get_cost(self):
        return self.price * self.quantity






