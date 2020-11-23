from django.db import models
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from colorfield.fields import ColorField
from shop.models import Trouser, TrouserVariant
from rad.utils import images_directory_path
from sorl.thumbnail import ImageField
import webcolors
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

    

