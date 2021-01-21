# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from functools import wraps

import webcolors
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from contents.models import ShopIndex
from menu.models import Menu
from shop.models import Image, Product, Trouser, TrouserVariant, Wavecap, WavecapVariant

from .pagination import StandardResultsSetPagination
from .serializers import ProductSerializer, TrouserDetailSerializer, TrouserSearchSerializer, TrouserSerializer, WavecapSerializer, WavecapDetailSerializer

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class HomeView(TemplateView):
    template_name = "shop/index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.home = ShopIndex.objects.all().prefetch_related('features').first()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home'] = self.home
        return context

class NewArrivalsListing(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryList = Product.objects.new_arrivals(num=10)
        return queryList

class BestSellerListing(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryList = Product.objects.bestseller(num=10)
        return queryList

class ProductByCategory(TemplateView):
    template_name = 'shop/item_by_category.html'  
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        title=""
        category_slug = self.kwargs["first_slug"]
        if category_slug:
            try:
                sub_category_slug = self.kwargs["second_slug"]
            except KeyError:
                sub_category_slug = None
            if sub_category_slug:
                title = sub_category_slug.replace("-", " ").upper()
                context['sub_category_slug'] = sub_category_slug
            else:
                title = category_slug.replace("-", " ").upper()
        context['title'] = title
        context['category_slug'] = category_slug
        return context

class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
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
    
    @paginate
    @action(methods=['get'], detail=False)
    def new_arrivals(self, request):
        queryset = Product.objects.new_arrivals()
        return queryset

    @paginate
    @action(methods=['get'], detail=False)
    def bestsellers(self, request):
        queryset = Product.objects.bestseller()
        return queryset
    
    @paginate
    @action(methods=['get'], detail=False)
    def featured(self, request):
        queryset = Product.objects.featured()
        return queryset
    
    @paginate
    @action(methods=['get'], detail=False)
    def back_in_stock(self, request):
        queryset = Product.objects.is_back()
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
    
    queryset = Trouser.objects.all()
    serializer_class = TrouserSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return TrouserSerializer
        else:
            return TrouserDetailSerializer
        return super().get_serializer_class()

    @action(methods=['get'], detail=False, url_path="")
    def trouser_by_category(self, request, **kwargs):
        is_back_products = Trousers.objects.is_back()
        temp = TrouserSerializer(trousers, many=True)
        return Response(temp.data)

class WavecapViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Wavecap.objects.all()
    serializer_class = WavecapSerializer
    pagination_class = StandardResultsSetPagination

class ProductListing(ListAPIView):
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.kwargs["first_slug"] == 'cargo-collections':
            return TrouserSerializer
        elif self.kwargs["first_slug"] == 'wave-cap-collections':
            return WavecapSerializer
        else:
            return ProductSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['page'] = self.kwargs["first_slug"]
        return response

class ProductDetail(TemplateView):
    template_name = 'shop/item_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['product_slug'] = self.kwargs['product_slug']
        return context

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

class TrouserSearchList(ListAPIView):
    # pagination_class = StandardResultsSetPagination
    serializer_class = TrouserSearchSerializer

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

def handler404(request, exception):
    return render(request, 'error.html', {'error': '404', 'error_message': '404, Page Not Found'}, status=404)

def handler400(request, exception):
    return render(request, 'error.html', {'error': '400', 'error_message': '400, Bad Request'}, status=400)

def handler500(request):
    return render(request, 'error.html', {'error': '500', 'error_message': '500, Internal Server Error'}, status=500)