# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import webcolors
from rest_framework.generics import ListAPIView, RetrieveAPIView

from contents.models import ShopIndex
from menu.models import Menu
from shop.models import Image, Product, Trouser, TrouserVariant, Wavecap, WavecapVariant

from .pagination import StandardResultsSetPagination
from .serializers import ProductSerializer, TrouserDetailSerializer, TrouserSearchSerializer, TrouserSerializer, WavecapSerializer

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
        if category_slug == 'new-arrivals' or category_slug == 'best-sellers' or category_slug == 'back-in-stock':
            if category_slug == 'new-arrivals':
                title = "NEW ARRIVALS"
            else:
                if category_slug == 'best-sellers':
                    title = "BEST SELLERS"
                else:
                    title = "BACK IN STOCK"
        else:
            try:
                sub_category_slug = self.kwargs["second_slug"]
            except KeyError:
                sub_category_slug = None
            if sub_category_slug:
                title = sub_category_slug.replace("-", " ").upper()
                context['sub_category_slug'] = sub_category_slug
            elif category_slug == 'collections':
                title = "ALL"
            else:
                raise Http404()
        context['title'] = title
        context['category_slug'] = category_slug
        return context

class ProductListing(ListAPIView):
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.kwargs["first_slug"] == 'new-arrivals' or self.kwargs["first_slug"] == 'best-sellers' or self.kwargs["first_slug"] == 'is-back':
            return ProductSerializer
        elif self.kwargs["first_slug"] == 'wavecao-collections':
            return WavecapSerializer
        else:
            return TrouserSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['page'] = self.kwargs["first_slug"]
        return response

    def get_queryset(self):
        if self.request.is_ajax() or True:
            category_slug = self.kwargs["first_slug"]
            if category_slug == 'new-arrivals' or category_slug == 'best-sellers' or category_slug == 'back-in-stock':
                if category_slug == 'new-arrivals':
                    queryList = Product.objects.new_arrivals()
                else:
                    if category_slug == 'best-sellers':
                        queryList = Product.objects.bestseller()
                    else:
                        queryList = Product.objects.is_back()
            elif category_slug == 'wavecap-collections':
                queryList = Wavecap.objects.filter(available=True)
            else:            
                try:
                    sub_category_slug = self.kwargs["second_slug"]
                except KeyError:
                    sub_category_slug = None
                if sub_category_slug:
                    try:
                        parent = Menu.objects.get(parent=None, slug=category_slug)
                        sub_category = Menu.objects.get(parent=parent, slug=sub_category_slug)
                    except ObjectDoesNotExist:
                        raise Http404()
                    else:
                        queryList = Trouser.objects.filter(category=sub_category).prefetch_related('trouser_variants', 'trouser_variants__trouser_variant_meta', 'variant__trouser_variant_images')
                elif category_slug == 'collections':
                    queryList = Trouser.objects.all().prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')
                else:
                    raise Http404()
            return queryList
        raise Http404()

class TrouserDetail(TemplateView):
    template_name = 'shop/item_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

class TrouserDetailAPI(RetrieveAPIView):
    serializer_class = TrouserDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Trouser.objects.all().prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')

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