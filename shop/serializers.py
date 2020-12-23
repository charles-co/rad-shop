from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from contents.models import Image
from menu.models import Menu

from .models import Trouser, TrouserMETA, TrouserVariant


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

# INDEX

class IndexTrouserVariantSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    color = serializers.CharField(source='get_color_name', read_only=True)
    
    class Meta:
        model = TrouserVariant
        fields = ("id", "color", "price", "old_price", "first_image",)
    
    def get_first_image(self, obj):
        first_image = Image.objects.filter(trouser_variant=obj).latest('id')
        first_image_serializer = ImageSerializer(first_image)
        return first_image_serializer.data

class IndexTrouserSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    first_variant = serializers.SerializerMethodField()

    class Meta:
        model = Trouser
        fields = ("id", "name", "url", "first_variant", "created_at")

    def get_first_variant(self, obj):
        first_variant = TrouserVariant.objects.filter(trouser=obj).latest('id')
        first_variant_serializer = IndexTrouserVariantSerializer(first_variant)
        return first_variant_serializer.data

# LIST

class TrouserVariantSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    first_meta = serializers.SerializerMethodField()
    color = serializers.CharField(source='get_color_name', read_only=True)
    
    class Meta:
        model = TrouserVariant
        fields = ("id", "first_meta", "price", "color", "first_image",)
    
    def get_first_image(self, obj):
        first_image = Image.objects.filter(trouser_variant=obj).earliest('id')
        first_image_serializer = ImageSerializer(first_image)
        return first_image_serializer.data
    
    def get_first_meta(self, obj):
        first_meta = TrouserMETA.objects.filter(trouser_variant=obj).earliest('id')
        first_meta_serializer = TrouserMETASerializer(first_meta)
        return first_meta_serializer.data

class TrouserSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    first_variant = serializers.SerializerMethodField()

    class Meta:
        model = Trouser
        fields = ("id", "name", "slug", "category", "first_variant", "is_featured", "is_bestseller", "created_at")

    def get_first_variant(self, obj):
        first_variant = TrouserVariant.objects.filter(trouser=obj).earliest('id')
        first_variant_serializer = TrouserVariantSerializer(first_variant)
        return first_variant_serializer.data


#DETAIL SERIALIZERS

class ImageDetailSerializer(serializers.HyperlinkedModelSerializer):
    file = HyperlinkedSorlImageField('300x400', options={"crop": "center", "quality": 99}, read_only=True)
    thumbnail = HyperlinkedSorlImageField('60x60', options={"crop": "center", "quality": 99}, source='file', read_only=True)
    
    class Meta:
        model = Image
        fields = ("id", "file", "thumbnail",)

class TrouserVariantTagSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    color = serializers.CharField(source='get_color_name', read_only=True)

    class Meta:
        model = TrouserVariant
        fields = ("id", "price", "color", "first_image",)
    
    def get_first_image(self, obj):
        first_image = Image.objects.filter(trouser_variant=obj).earliest('id')
        first_image_serializer = ImageSerializer(first_image)
        return first_image_serializer.data

class TrouserTagSerializer(serializers.ModelSerializer):
    first_variant = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Trouser
        fields = ("id", "name", "slug", "first_variant", "url")

    def get_first_variant(self, obj):
        first_variant = TrouserVariant.objects.filter(trouser=obj).earliest('id')
        first_variant_serializer = TrouserVariantTagSerializer(first_variant)
        return first_variant_serializer.data

class TrouserVariantDetailSerializer(serializers.ModelSerializer):
    trouser_variant_images = ImageDetailSerializer(many=True)
    trouser_variant_meta = TrouserMETASerializer(many=True)
    color = serializers.CharField(source='get_color_name', read_only=True)

    class Meta:
        model = TrouserVariant
        fields = ("id", "trouser_variant_images", "trouser_variant_meta", "price", "color")


class TrouserDetailSerializer(serializers.ModelSerializer):
    variant = TrouserVariantDetailSerializer(many=True, read_only=True)
    similiar_trousers = serializers.SerializerMethodField()
    description = serializers.CharField(source='get_markdown', read_only=True)

    class Meta:
        model = Trouser
        fields = ("id", "name", "slug", "description", "variant", "similiar_trousers")

    def get_similiar_trousers(self, obj):
        similiar_trousers = Trouser.objects.get(id=obj.id).tags.similar_objects()[:8]
        similiar_trousers_serializer = TrouserTagSerializer(similiar_trousers, many=True)
        return similiar_trousers_serializer.data


#SEARCH SERIALIZER

class ImageSearchSerializer(serializers.HyperlinkedModelSerializer):
    file = HyperlinkedSorlImageField('90x120', options={"crop": "center", "quality": 99}, read_only=True)
    file_sm = HyperlinkedSorlImageField('60x80', options={"crop": "center", "quality": 99}, source='file', read_only=True)

    class Meta:
        model = Image
        fields = ("id", "file", "file_sm")

class TrouserVariantSearchSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    color = serializers.CharField(source='get_color_name', read_only=True)

    class Meta:
        model = TrouserVariant
        fields = ("id", "price", "color", "first_image",)
    
    def get_first_image(self, obj):
        first_image = Image.objects.filter(trouser_variant=obj).earliest('id')
        first_image_serializer = ImageSearchSerializer(first_image)
        return first_image_serializer.data
    
class TrouserSearchSerializer(serializers.ModelSerializer):
    variant = TrouserVariantSearchSerializer(many=True, read_only=True)
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Trouser
        fields = ("id", "name", "url", "variant")
