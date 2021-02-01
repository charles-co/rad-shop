from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
# from django.contrib.contenttypes.fields import GenericRelation
from django.utils.safestring import mark_safe

import webcolors
from colorfield.fields import ColorField
from mptt.models import MPTTModel, TreeForeignKey
# from .utils import images_directory_path
# from .fields import OrderField
# from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from menu.models import Menu
from rad.utils import images_directory_path

# Create your models here.
class ItemBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        abstract = True
        
    # def render(self):
    #     return render_to_string('products/content/{}.html'.format(self._meta.model_name), {'item': self})

class Image(ItemBase):

    file = ImageField(upload_to=images_directory_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('trouservariant','wavecapvariant')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.item.__str__()

class ProductQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(available=True).prefetch_related('item')

    def new_arrivals(self, num):
        if num == -1:
            return self.order_by("-created_at")
        return self.order_by("-created_at")[:num]

    def featured(self):
        return self.filter(is_featured=True)
    
    def is_back(self):
        return self.filter(is_back=True)
    
    def is_bestseller(self, num):
        if num == -1:
            return self.filter(is_bestseller=True)
        return self.filter(is_bestseller=True)[:num]
    
    def is_discounted(self):
        return self.filter(is_discounted=True)

    def search(self, query):
        lookups =   (   Q(name__icontains=query) | 
                        Q(trouser__description__icontains=query) |
                        Q(wavecap__description__icontains=query) |
                        Q(trouser__variant__price__icontains=query) |
                        Q(wavecap__variant__price__icontains=query) |
                        Q(trouser__variant__color__icontains=query) |
                        Q(wavecap__variant__color__icontains=query) |
                        Q(trouser__tags__name__icontains=query) |
                        Q(wavecap__tags__name__icontains=query)
                    )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).prefetch_related('wavecap', 'wavecap__variants', 'trouser__variants', 'wavecap').distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def new_arrivals(self, num=-1):
        return self.get_queryset().active().new_arrivals(num)

    def featured(self):
        return self.get_queryset().active().featured()
    
    def bestseller(self, num=-1):
        return self.get_queryset().active().is_bestseller(num)

    def is_back(self):
        return self.get_queryset().active().is_back()

    def discounted(self):
        return self.get_queryset().is_discounted()

    # def get_by_id(self, id):
    #     qs = self.get_queryset().filter(id=id) # Trouser.objects == self.get_queryset()
    #     if qs.count() == 1:
    #         return qs.first()
    #     return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):

    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_bestseller = models.BooleanField(default=False)
    is_back = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('trouser','wavecap')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    objects = ProductManager()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.item.name

class BrandQuerySet(models.query.QuerySet):

    def featured(self):
        return self.filter(is_featured=True)

    def by_category(self, category):
        category = Menu.objects.filter(slug=category).first()
        return self.filter(category=category)

    def search(self, query):
        lookups = (Q(name__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(variant__price__icontains=query) |
                  Q(variant__color__icontains=query) |
                  Q(tags__name__icontains=query)
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()

class BrandManager(models.Manager):

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Trouser.objects.featured() 
        return self.get_queryset().active().featured()
    
    def by_category(self, category):
        return self.get_queryset().active().by_category(category)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Trouser.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class Brand(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    category = TreeForeignKey(Menu, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)ss_related")
    description = HTMLField(null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_back = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    tags = TaggableManager(blank=True)

    class MPTTMeta:
        abstract = True
        order_insertion_by = ['name', '-created']
    
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail', args=[self.get_product_name(), self.slug])
    
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def discounted_percentage(self):
        if self.is_discounted and self.old_price < self.price:
            return (self.price / self.old_price * 100)

    def get_markdown(self):
        return mark_safe(self.description)

    def get_color_name(self):
        return webcolors.hex_to_name(self.color).title()
    
    def get_random_char(self):
        return str(self.id) + self.__class__.__name__
    
    def get_product_name(self):
        return self.__class__.__name__.lower()

class BrandVariant(models.Model):

    color = ColorField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)

    class Meta:
        abstract = True
        ordering = ['id']
        
    def get_color_name(self):
        return webcolors.hex_to_name(self.color).title()
    
class BrandMETA(models.Model):
    SIZE_CHOICES = [
        ('30', '30W'),
        ('32', '32W'),
        ('34', '34W'),
        ('36', '36W'),
        ('38', '38W'),
        ('40', '40W'),
        ('42', '42W'),
    ]
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=1)
    
    class Meta:
        abstract = True
        ordering = ['size',]

class TrouserQuerySet(BrandQuerySet):

    def active(self):
        return self.filter(available=True).prefetch_related('variants', 'variants__metas', 'variants__images')

class TrouserManager(BrandManager):
    
    def get_queryset(self):
        return TrouserQuerySet(self.model, using=self._db)

class Trouser(Brand):
    products = GenericRelation(Product, related_query_name="%(class)s")

    objects = TrouserManager()

class TrouserVariant(BrandVariant):
    trouser = models.ForeignKey(Trouser, on_delete=models.CASCADE, related_name="variants")
    images = GenericRelation(Image, related_query_name="%(class)s")

    class Meta(BrandVariant.Meta):
        constraints = [
            models.UniqueConstraint(fields=['trouser', 'color'], name='unique trouser color')
        ]

    def __str__(self):
        return self.trouser.__str__()

    def get_absolute_url(self):
        return self.trouser.get_absolute_url()

class TrouserMETA(BrandMETA):
    trouser_variant = models.ForeignKey(TrouserVariant, on_delete=models.CASCADE, related_name="metas")

    class Meta(BrandMETA.Meta):
        constraints = [
            models.UniqueConstraint(fields=['trouser_variant', 'size'], name='unique size')
        ]
    
    def __str__(self):
        return self.trouser_variant.__str__()

class WavecapQuerySet(BrandQuerySet):

    def active(self):
        return self.filter(available=True).prefetch_related('variants', 'variants__images')

class WavecapManager(BrandManager):
    
    def get_queryset(self):
        return WavecapQuerySet(self.model, using=self._db)

class Wavecap(Brand):
    products = GenericRelation(Product, related_query_name="%(class)s")

    objects = WavecapManager()

class WavecapVariant(BrandVariant):
    wavecap = models.ForeignKey(Wavecap, on_delete=models.CASCADE, related_name="variants")
    images = GenericRelation(Image, related_query_name="%(class)s")
    stock = models.PositiveIntegerField(default=1)

    class Meta(BrandVariant.Meta):
        constraints = [
            models.UniqueConstraint(fields=['wavecap', 'color'], name='unique wavecap color')
        ]

    def __str__(self):
        return self.wavecap.__str__()
    
    def get_absolute_url(self):
        return self.wavecap.get_absolute_url()