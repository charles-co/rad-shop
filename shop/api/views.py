from django.db.models import QuerySet, Q
from django.http import JsonResponse
from django.templatetags.static import static

from functools import wraps

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from contents.models import ShopIndex
from shop.models import Product, Trouser, TrouserVariant, Wavecap, WavecapVariant

from .pagination import StandardResultsSetPagination
from .serializers import ProductSerializer, TrouserDetailSerializer, TrouserSerializer, WavecapSerializer, WavecapDetailSerializer

import webcolors 

def paginate(func):
    
        @wraps(func)
        def inner(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            assert isinstance(queryset, (list, QuerySet)),  "apply_paginations expects a list or queryset"

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data) 

            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return inner

class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def paginate(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            assert isinstance(queryset, (list, QuerySet)),  "apply_paginations expects a list or queryset"

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                products_obj = [list(x.values())[0] for x in serializer.data]
                return self.get_paginated_response(products_obj) 

            serializer = self.get_serializer(products, many=True)
            products_obj = [list(x.values())[0] for x in serializer.data]
            return Response(products_obj)
        return inner

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        if self.action == 'list':
            color = self.request.GET.get('color', 'all')
            order = self.request.GET.get('order_by', 'name')
            order= "".join(order.split('variants__'))
            if color == 'all':
                queryList = Product.objects.order_by(order)
            else:
                print('Here')
                color_hex = webcolors.name_to_hex(color).upper()
                queryList = Product.objects.filter(Q(trouser__variants__color=color_hex) | Q(wavecap__variants__color=color_hex)).order_by(order)
        else:
            queryList = Product.objects.all()
        return queryList

    @paginate
    def list(self, request):
        print(request.GET)
        queryset = self.get_queryset()
        return queryset

    @paginate
    @action(methods=['get'], detail=False)
    def new_arrivals(self, request):
        color = self.request.GET.get('color', 'all')
        order = self.request.GET.get('order_by', 'name')
        order= "".join(order.split('variants__'))
        if color == 'all':
            queryset = Product.objects.new_arrivals().order_by(order)[:20]
        else:
            color_hex = webcolors.name_to_hex(color).upper()
            queryset = Product.objects.new_arrivals().filter(Q(trouser__variants__color=color_hex) | Q(wavecap__variants__color=color_hex)).order_by(order)[:20]
        
        return queryset

    @paginate
    @action(methods=['get'], detail=False)
    def bestsellers(self, request):
        color = self.request.GET.get('color', 'all')
        order = self.request.GET.get('order_by', 'name')
        order= "".join(order.split('variants__'))
        if color == 'all':
            queryset = Product.objects.bestseller().order_by(order)
        else:
            color_hex = webcolors.name_to_hex(color).upper()
            queryset = Product.objects.bestseller().filter(Q(trouser__variants__color=color_hex) | Q(wavecap__variants__color=color_hex)).order_by(order)
        return queryset
    
    @paginate
    @action(methods=['get'], detail=False)
    def featured(self, request):
        queryset = Product.objects.featured()
        return queryset
    
    @paginate
    @action(methods=['get'], detail=False)
    def back_in_stock(self, request):
        color = self.request.GET.get('color', 'all')
        order = self.request.GET.get('order_by', 'name')
        order= "".join(order.split('variants__'))
        if color == 'all':
            queryset = Product.objects.is_back().order_by(order)
        else:
            color_hex = webcolors.name_to_hex(color).upper()
            queryset = Product.objects.is_back().filter(Q(trouser__variants__color=color_hex) | Q(wavecap__variants__color=color_hex)).order_by(order)
        return queryset

    @action(methods=['get'], detail=False, url_path="category/(?P<first_slug>[-\w]+)(?:/(?P<second_slug>[-\w]+))?")
    def by_category(self, request, first_slug=None, second_slug=None):
        all_products = ['new-arrivals', 'best-sellers', 'back-in-stock']
        specific = ['cargo-collections', 'wave-cap-collections']
        if first_slug in all_products:
            if first_slug == all_products[0]:
                return self.new_arrivals(request)
            elif first_slug == all_products[1]:
                return self.bestsellers(request)
            else:
                return self.back_in_stock(request)

    @action(methods=['get'], detail=False, url_path="slideshow/(?P<first_slug>[-\w]+)")
    def slideshow(self, request, first_slug=None):
        slideshows = ['new-arrivals', 'best-sellers']
        if first_slug in slideshows:
            if first_slug == slideshows[0]:
                queryset = Product.objects.new_arrivals(10)
            else:
                queryset = Product.objects.bestseller(10)

        serializer = self.get_serializer(queryset, many=True)
        products_obj = [list(x.values())[0] for x in serializer.data]
        
        return Response(products_obj)

        # elif first_slug in specific:
        #     if first_slug == specific[0]:
        #         products = Product.objects.all().order_by('-created_at')
        #     elif first_slug == all_products[1]:
        #         products = Product.objects.bestseller()

class TrouserViewSet(viewsets.ReadOnlyModelViewSet):
    
    # queryset = Trouser.objects.all()
    # serializer_class = TrouserSerializer
    pagination_class = StandardResultsSetPagination
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            color = self.request.GET.get('color', 'all')
            order = self.request.GET.get('order_by', 'name')
            if color == 'all':
                queryList = Trouser.objects.order_by(order)
            else:
                color_hex = webcolors.name_to_hex(color).upper()
                queryList = Trouser.objects.filter(variants__color=color_hex).order_by(order)
        else:
            queryList = Trouser.objects.all()
        return queryList

    def get_serializer_class(self):
        listItems = ['by_category', 'list']
        if self.action in listItems:
            return TrouserSerializer
        else:
            return TrouserDetailSerializer
        return super().get_serializer_class()

    @action(methods=['get'], detail=False, url_path="")
    def trouser_by_category(self, request, **kwargs):
        is_back_products = Trousers.objects.is_back()
        temp = TrouserSerializer(trousers, many=True)
        return Response(temp.data)

    @paginate
    @action(methods=['get'], detail=False, url_path="category/(?P<first_slug>[-\w]+)(?:/(?P<second_slug>[-\w]+))?")
    def by_category(self, request, first_slug=None, second_slug=None):
        querylist = Trouser.objects.by_category(first_slug)
        return querylist

class WavecapViewSet(viewsets.ReadOnlyModelViewSet):
    
    # queryset = Wavecap.objects.all()
    pagination_class = StandardResultsSetPagination
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
    def get_queryset(self):
        color = self.request.GET.get('color', 'all')
        order = self.request.GET.get('order_by', 'name')
        if self.action == 'list':
            if color == 'all':
                queryList = Wavecap.objects.order_by(order)
            else:
                color_hex = webcolors.name_to_hex(color).upper()
                queryList = Wavecap.objects.filter(variants__color=color_hex).order_by(order)
        else:
            queryList = Wavecap.objects.all()
        return queryList
    
    def get_serializer_class(self):
        if self.action == 'list':
            return WavecapSerializer
        else:
            return WavecapDetailSerializer
        return super().get_serializer_class()

class ProductDetailAPI(RetrieveAPIView):
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_serializer_class(self):
        if self.kwargs["product_slug"] == 'trouser':
            return TrouserDetailSerializer
        elif self.kwargs["product_slug"] == 'wavecap':
            return WavecapDetailSerializer
        else:
            print("omo")
        return super().get_serializer_class()

    def get_queryset(self):
        print(self.kwargs)
        if self.kwargs['product_slug'] == 'trouser':
            queryList = Trouser.objects.all()
        elif self.kwargs['product_slug'] == 'wavecap':
            queryList = Wavecap.objects.all()
        return queryList

class ProductSearchList(ListAPIView):
    # pagination_class = StandardResultsSetPagination
    # serializer_class = ProductSearchSerializer

    def get_queryset(self):
        request = self.request
        if request.is_ajax():
            query = request.GET.get("query", None)
            query = query.strip()
            if query is not None and query != "":
                queryList = Trouser.objects.search(query)
            else:
                queryList = Trouser.objects.featured().prefetch_related('variant')
            return queryList

def getColors(request):
    trousers = list(TrouserVariant.objects.all().values_list('color', flat=True).distinct())
    wavecaps = list(WavecapVariant.objects.all().values_list('color', flat=True).distinct())
    temp = set(trousers + wavecaps)
    colors = [webcolors.hex_to_name(x).title() for x in temp]
    return JsonResponse(colors, safe=False)

def getIndexSlideshow(request):
    images = list(ShopIndex.objects.values_list("image1", "image2", "image3"))[0]
    x = [{"src" : "/media/" + x} for x in images]
    result = {"images": x, "overlay": static("js/overlays/03.png")}
    return JsonResponse(result, safe=False)