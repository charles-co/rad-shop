from django.contrib import admin

from nested_admin import (NestedGenericStackedInline, NestedInlineModelAdmin,
                          NestedModelAdmin, NestedStackedInline,
                          NestedTabularInline)
from sorl.thumbnail.admin import AdminImageMixin

from shop.forms import TrouserForm
from shop.models import Image, Product, Trouser, TrouserMETA, TrouserVariant, Wavecap, WavecapVariant

# from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline

# Register your models here.

class ImageInline(AdminImageMixin, NestedGenericStackedInline):
    model = Image
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'created_at']
    list_filter = ['created_at', 'updated_at']
    # list_editable = ['available']

    def get_name(self, obj):
        return obj.item.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'item__name'

class TrouserMETAInline(NestedStackedInline):
    model = TrouserMETA
    extra = 1

class TrouserVariantInline(AdminImageMixin, NestedStackedInline):
    model = TrouserVariant
    inlines = [TrouserMETAInline, ImageInline,]
    extra = 1

class TrouserAdmin(NestedModelAdmin):
    model = Trouser
    form = TrouserForm
    list_display = ['name', 'available', 'created_at', 'slug']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['available']
    inlines = [TrouserVariantInline,]

class WavecapVariantInline(AdminImageMixin, NestedStackedInline):
    model = WavecapVariant
    inlines = [ImageInline,]
    extra = 1

class WavecapAdmin(NestedModelAdmin):
    model = Wavecap
    list_display = ['name', 'available', 'created_at', 'slug']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['available']
    inlines = [WavecapVariantInline,]

admin.site.register(Trouser, TrouserAdmin)
admin.site.register(Wavecap, WavecapAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(TrouserMETA)


