from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
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
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from menu.models import Menu

# Create your models here.


class Trouser(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    category = TreeForeignKey(Menu, related_name='trousercategory', on_delete=models.CASCADE)
    description = HTMLField(null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_back = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    tags = TaggableManager()

    class MPTTMeta:
        order_insertion_by = ['name', '-created']
    
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail', args=[self.slug])
    
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

class TrouserVariant(models.Model):

    trouser = models.ForeignKey(Trouser, on_delete=models.CASCADE, related_name="variant")
    color = ColorField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trouser', 'color'], name='unique color')
        ]

    def __str__(self):
        return "{} {}".format(self.get_color_name(), self.trouser.name)
        
    def get_color_name(self):
        return webcolors.hex_to_name(self.color).title()
    
class TrouserMETA(models.Model):
    SIZE_CHOICES = [
        ('30', '30W'),
        ('32', '32W'),
        ('34', '34W'),
        ('36', '36W'),
        ('38', '38W'),
        ('40', '40W'),
        ('42', '42W'),
    ]
    trouser_variant = models.ForeignKey(TrouserVariant, on_delete=models.CASCADE, related_name='trouser_variant_meta')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['size',]
        constraints = [
            models.UniqueConstraint(fields=['trouser_variant', 'size'], name='unique size')
        ]

    def __str__(self):
        return self.trouser_variant.__str__()


    
    
