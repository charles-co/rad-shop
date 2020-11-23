from django.contrib import admin
# from products.forms import ProductBodyForm
from menu.models import Menu
from mptt.admin import DraggableMPTTAdmin
# from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline

# Register your models here.

class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'name', 'slug',)
    list_display_links = ('indented_title',)

# class ImageInline(GenericStackedInline):
#     model = Image
#     extra = 1

# class VideoInline(GenericStackedInline):
#     model = Video
#     extra = 1

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductBodyForm
#     list_display = ('name', 'created', 'updated', 'price', 'slug',)
#     search_fields = ('name', 'price')
#     inlines = [ImageInline, VideoInline]
    
#     class Media:
#        pass

# admin.site.register(Image)
# admin.site.register(Video)
# admin.site.register(Product, ProductAdmin)
admin.site.register(Menu, MenuAdmin)
