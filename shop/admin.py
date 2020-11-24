from django.contrib import admin

from nested_admin import (NestedGenericStackedInline, NestedInlineModelAdmin,
                          NestedModelAdmin, NestedStackedInline,
                          NestedTabularInline)
from sorl.thumbnail.admin import AdminImageMixin

from contents.models import Image
from shop.forms import TrouserForm
from shop.models import Trouser, TrouserMETA, TrouserVariant

# from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline

# Register your models here.

class ImageInline(AdminImageMixin, NestedStackedInline):
    model = Image
    extra = 1

class TrouserMETAInline(NestedStackedInline):
    model = TrouserMETA
    extra = 1

class TrouserVariantInline(NestedStackedInline):
    model = TrouserVariant
    inlines = [TrouserMETAInline, ImageInline,]
    extra = 1

class TrouserAdmin(NestedModelAdmin):
    model = Trouser
    form = TrouserForm
    list_display = ['name', 'available', 'created', 'slug']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    inlines = [TrouserVariantInline,]

admin.site.register(Trouser, TrouserAdmin)
# admin.site.register(TrouserMETA)


