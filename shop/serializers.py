from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import Trouser, TrouserMETA, TrouserVariant
from menu.models import Menu
from rest_framework_recursive.fields import RecursiveField
from contents.models import Image
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('slug',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id","file",)

class TrouserMETASerializer(serializers.ModelSerializer):
    class Meta:
        model = TrouserMETA
        fields = ("id", "size", "stock",)

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
        fields = ("id", "name", "slug", "category", "first_variant", "is_featured", "is_bestseller", "created")

    def get_first_variant(self, obj):
        first_variant = TrouserVariant.objects.filter(trouser=obj).earliest('id')
        print(type(first_variant))
        first_variant_serializer = TrouserVariantSerializer(first_variant)
        return first_variant_serializer.data

###################################################################################

class ImageDetailSerializer(serializers.HyperlinkedModelSerializer):
    file = HyperlinkedSorlImageField('300x400', options={"crop": "center", "quality": 100, "format": "PNG"}, read_only=True)
    thumbnail = HyperlinkedSorlImageField('60x60', options={"crop": "center", "quality": 100, "format": "PNG"}, source='file', read_only=True)
    
    class Meta:
        model = Image
        fields = ("id", "file", "thumbnail")

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

    class Meta:
        model = Trouser
        fields = ("id", "name", "slug", "first_variant")

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
