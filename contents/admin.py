from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from nested_admin import (NestedGenericStackedInline, NestedInlineModelAdmin,
                          NestedModelAdmin, NestedStackedInline,
                          NestedTabularInline, NestedGenericTabularInline)
from sorl.thumbnail.admin import AdminImageMixin

from contents.models import ShopIndex, ShopIndexFeature
# from .models import Color
# Register your models here.

# class ImageInline(AdminImageMixin, NestedGenericTabularInline):
#     model = ShopPageImage
#     extra = 1

# class FeaturesInline(AdminImageMixin, admin.StackedInline):
#     model = ShopIndexFeature
#     extra = 1

# class ShopIndexFeaturesAdmin(admin.ModelAdmin):
#     inlines = [ImageInline,]
#     extra = 1

class ShopIndexAdmin(AdminImageMixin, admin.ModelAdmin):
    pass

admin.site.register(ShopIndex, ShopIndexAdmin)
admin.site.register(ShopIndexFeature)
# admin.site.register(ShopIndexFeature, ShopIndexFeaturesAdmin)
# admin.site.register(ShopPageImage)