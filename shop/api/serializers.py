from django.contrib.contenttypes.models import ContentType
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from menu.models import Menu

from shop.models import Image, Product, Trouser, TrouserMETA, TrouserVariant, Wavecap, WavecapVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('slug',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "file",)

class TrouserMETASerializer(serializers.ModelSerializer):
    class Meta:
        model = TrouserMETA
        fields = ("id", "size", "stock",)

# INDEX & LIST SERIALIZER

class BaseVariantSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    color = serializers.CharField(source='get_color_name', read_only=True)
    
    class Meta:
        fields = ("id", "color", "price", "old_price", "first_image",)
    
    def get_first_image(self, obj):
        item_type = ContentType.objects.get_for_model(obj)
        first_image = Image.objects.filter(content_type__pk=item_type.id, object_id=obj.id).earliest('id')
        first_image_serializer = ImageSerializer(first_image)
        return first_image_serializer.data

class BaseSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    category = CategorySerializer(read_only=True)
    first_variant = serializers.SerializerMethodField()
    sku = serializers.CharField(source='get_random_char', read_only=True)
    product = serializers.CharField(source='get_product_name', read_only=True)
    colors = serializers.SlugRelatedField(source='variants', slug_field='color', read_only=True, many=True)

    class Meta:
        fields = ("id", "name", "url", "category", "sku", "slug", "product", "colors", "first_variant", "is_featured", "is_bestseller", "created_at")

class TrouserVariantSerializer(BaseVariantSerializer):
    color = serializers.CharField(source='get_color_name', read_only=True)
    
    class Meta(BaseVariantSerializer.Meta):
        model = TrouserVariant

class TrouserSerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Trouser

    def get_first_variant(self, obj):
        first_variant = TrouserVariant.objects.filter(trouser=obj).earliest('id')
        first_variant_serializer = TrouserVariantSerializer(first_variant)
        return first_variant_serializer.data

class WavecapVariantSerializer(BaseVariantSerializer):
    color = serializers.CharField(source='get_color_name', read_only=True)
    
    class Meta(BaseVariantSerializer.Meta):
        model = WavecapVariant

class WavecapSerializer(BaseSerializer):
    
    class Meta(BaseSerializer.Meta):
        model = Wavecap

    def get_first_variant(self, obj):
        first_variant = WavecapVariant.objects.filter(wavecap=obj).earliest('id')
        first_variant_serializer = WavecapVariantSerializer(first_variant)
        return first_variant_serializer.data

class ProductSerializer(serializers.ModelSerializer):
    
    item = GenericRelatedField({
        Trouser: TrouserSerializer(),
        Wavecap: WavecapSerializer(),
    })

    class Meta:
        model = Product
        fields = ("item",)

# DETAIL SERIALIZERS

class ImageDetailSerializer(serializers.HyperlinkedModelSerializer):
    file = HyperlinkedSorlImageField('300x400', options={"quality": 99, "format": "PNG"}, read_only=True)
    thumbnail = HyperlinkedSorlImageField('60x60', options={"quality": 99, "format": "PNG"}, source='file', read_only=True)
    
    class Meta:
        model = Image
        fields = ("id", "file", "thumbnail",)

class BaseVariantDetailSerializer(serializers.ModelSerializer):
    product_variant_images = ImageDetailSerializer(many=True)
    color = serializers.CharField(source='get_color_name', read_only=True)

class TrouserVariantDetailSerializer(BaseVariantDetailSerializer):
    metas = TrouserMETASerializer(many=True)
    images = ImageDetailSerializer(many=True)

    class Meta:
        model = TrouserVariant
        fields = ("id", "images", "metas", "price", "color")

class BaseDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='get_markdown', read_only=True)
    product = serializers.CharField(source='get_product_name', read_only=True)

    class Meta:
        fields = ("id", "name", "slug", "product", "description", "variants", "similiar_products")

class TrouserDetailSerializer(BaseDetailSerializer):
    variants = TrouserVariantDetailSerializer(many=True, read_only=True)
    similiar_products = serializers.SerializerMethodField()

    class Meta(BaseDetailSerializer.Meta):
        model = Trouser

    def get_similiar_products(self, obj):
        similiar_trousers = Trouser.objects.get(id=obj.id).tags.similar_objects()[:8]
        similiar_trousers_serializer = TrouserSerializer(similiar_trousers, many=True)
        return similiar_trousers_serializer.data

class WavecapVariantDetailSerializer(BaseVariantDetailSerializer):
    images = ImageDetailSerializer(many=True)
    class Meta:
        model = WavecapVariant
        fields = ("id", "images", "stock", "price", "color")

class WavecapDetailSerializer(BaseDetailSerializer):
    variants = WavecapVariantDetailSerializer(many=True, read_only=True)
    similiar_products = serializers.SerializerMethodField()

    class Meta(BaseDetailSerializer.Meta):
        model = Wavecap

    def get_similiar_products(self, obj):
        similiar_wavecaps = Wavecap.objects.get(id=obj.id).tags.similar_objects()[:8]
        similiar_wavecaps_serializer = WavecapSerializer(similiar_wavecaps, many=True)
        return similiar_wavecaps_serializer.data

#SEARCH SERIALIZER

# class ImageSearchSerializer(serializers.HyperlinkedModelSerializer):
#     file = HyperlinkedSorlImageField('90x120', options={"quality": 99, "format": "PNG"}, read_only=True)
#     file_sm = HyperlinkedSorlImageField('60x80', options={"quality": 99, "format": "PNG"}, source='file', read_only=True)

#     class Meta:
#         model = Image
#         fields = ("id", "file", "file_sm")

# class TrouserVariantSearchSerializer(serializers.ModelSerializer):
#     first_image = serializers.SerializerMethodField()
#     color = serializers.CharField(source='get_color_name', read_only=True)
#     other_colors = serializers.CharField(source='get_color_name', read_only=True)

#     class Meta:
#         model = TrouserVariant
#         fields = ("id", "price", "color", "first_image",)
    
#     def get_first_image(self, obj):
#         first_image = Image_Trouser.objects.filter(trouser_variant=obj).earliest('id')
#         first_image_serializer = ImageSearchSerializer(first_image)
#         return first_image_serializer.data
    
# class TrouserSearchSerializer(serializers.ModelSerializer):
#     variant = TrouserVariantSearchSerializer(many=True, read_only=True)
#     url = serializers.CharField(source='get_absolute_url')

#     class Meta:
#         model = Trouser
#         fields = ("id", "name", "url", "variant")
