from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Menu(MPTTModel):
    SHOP = 'SH'
    BLOG = 'BG'
    APP = [
        (SHOP, 'Shop'),
        (BLOG, 'Blog'),
    ]
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=50, db_index=True, blank=True, allow_unicode=True)
    app = models.CharField(max_length=2, choices=APP, default=SHOP)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', db_index=True)
    is_active = models.BooleanField(default=True)
    show_all = models.BooleanField('All products', default=False)
    
    class MPTTMeta:
        order_insertion_by = ['app', 'name']

    # def get_absolute_url(self):
    #     return reverse('blog:navigation',args=[self.slug])
        
    def __str__(self):
        return self.name
        
    @property
    def show_all_products(self):
        return self.show_all