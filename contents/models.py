from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import webcolors
from colorfield.fields import ColorField
from sorl.thumbnail import ImageField

from rad.utils import images_directory_path, shop_index_directory_path
from shop.models import Trouser, TrouserVariant
from tinymce.models import HTMLField

# Create your models here.

class ItemBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        abstract = True
        
    # def render(self):
    #     return render_to_string('products/content/{}.html'.format(self._meta.model_name), {'item': self})

    def __str__(self):
        return self.trouser_variant.__str__()

class Image(ItemBase):
    trouser_variant = models.ForeignKey(TrouserVariant, on_delete=models.CASCADE, related_name='trouser_variant_images')
    file = ImageField(upload_to=images_directory_path)

# class ShopPageImage(ItemBase):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('shopindexfeatures','shopindex')})
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     file = ImageField(upload_to=shop_index_directory_path)

#     def save(self, *args, **kwargs):
#         if self.content_object.__class__.__name__.lower() == "shopindexfeatures":
#             ct = ContentType.objects.get_for_model(self.content_object)
#             if self.__class__.objects.filter(content_type=ct, object_id=features_images__id).count() < 1:
#                 super().save(*args, **kwargs)
#         elif self.content_object.__class__.__name__.lower() == "shopindex":
#             ct = ContentType.objects.get_for_model(self.content_object)
#             if self.__class__.objects.filter(content_type=ct).count() < 4:
#                 super().save(*args, **kwargs)

class ShopIndex(models.Model):
    top_text = HTMLField(null=True, blank=True)
    info_text = HTMLField(null=True, blank=True)
    image1 = ImageField(upload_to=shop_index_directory_path)
    image2 = ImageField(null=True, blank=True, upload_to=shop_index_directory_path)
    image3 = ImageField(null=True, blank=True, upload_to=shop_index_directory_path)
    # image = GenericRelation(ShopPageImage, related_query_name="home_images")

    class Meta:
        verbose_name = "Index Page"
        verbose_name_plural = "Index Page"
        # verbose_plural = "Index Page"
    
    def __str__(self):
        return "Index Page"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() <= 1:
            print(self.__class__)
            print(self.__class__.__name__)
            super().save(*args, **kwargs)

    def get_markdown_top(self):
        return mark_safe(self.top_text)
    
    def get_markdown_info(self):
        return mark_safe(self.info_text)

class ShopIndexFeature(models.Model):
    shop_index = models.ForeignKey(ShopIndex, on_delete=models.CASCADE, related_name="features", null=True, blank=True)
    text = HTMLField(null=True, blank=True)
    url = models.URLField()
    image = ImageField(upload_to=shop_index_directory_path)
    # image = GenericRelation(ShopPageImage, related_query_name="features_images")
    
    class Meta:
        verbose_name = "Index Feature"
        verbose_name_plural = "Index Features"
        # verbose_plural = "Index Page"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() <= 4:
            print(self.__class__)
            print(self.__class__.__name__)
            super().save(*args, **kwargs)

    def get_markdown(self):
        return mark_safe(self.text)
