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
from tinymce.models import HTMLField

# Create your models here.

class ShopIndex(models.Model):
    top_text = HTMLField(null=True, blank=True)
    info_text = HTMLField(null=True, blank=True)
    image1 = ImageField(upload_to=shop_index_directory_path)
    image2 = ImageField(null=True, blank=True, upload_to=shop_index_directory_path)
    image3 = ImageField(null=True, blank=True, upload_to=shop_index_directory_path)

    class Meta:
        verbose_name = "Index Page"
        verbose_name_plural = "Index Page"
    
    def __str__(self):
        return "Index Page"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() < 1:
            super().save(*args, **kwargs)

    @property
    def get_markdown_top(self):
        return mark_safe(self.top_text)
    
    @property
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
    def __str__(self):
        return self.shop_index.__str__() + " Feature " + str(self.id)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() <= 4:
            super().save(*args, **kwargs)

    def get_markdown(self):
        return mark_safe(self.text)
