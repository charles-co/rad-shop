# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import webcolors
from rest_framework.generics import ListAPIView, RetrieveAPIView

from cart.forms import CartAddProductForm
from contents.models import Image
from menu.models import Menu
from shop.models import Trouser, TrouserVariant

from .pagination import StandardResultsSetPagination
from .serializers import TrouserDetailSerializer, TrouserSerializer


class HomeView(TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TrouserByCategory(TemplateView):
    template_name = 'shop/item_by_category.html'  
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        title=""
        category_slug = self.kwargs["first_slug"]
        if category_slug == 'new-arrivals' or category_slug == 'bestsellers' or category_slug == 'back-in-stock':
            if category_slug == 'new-arrivals':
                title = "NEW ARRIVALS"
            else:
                if category_slug == 'bestsellers':
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
            else:
                title = "ALL"
        context['title'] = title
        context['category_slug'] = category_slug
        return context

class TrouserListing(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = TrouserSerializer

    def get_queryset(self):
        category_slug = self.kwargs["first_slug"]
        if category_slug == 'new-arrivals' or category_slug == 'bestsellers' or category_slug == 'back-in-stock':
            if category_slug == 'new-arrivals':
                queryList = Trouser.objects.order_by("-created").prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')

            else:
                if category_slug == 'bestsellers':
                   queryList = Trouser.objects.filter(is_bestseller=True).prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')
                else:
                    queryList = Trouser.objects.filter(is_back=True).prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')
        else:            
            try:
                sub_category_slug = self.kwargs["second_slug"]
            except KeyError:
                sub_category_slug = None
            if sub_category_slug:
                parent = Menu.objects.get(parent=None, slug=category_slug)
                sub_category = Menu.objects.get(parent=parent, slug=sub_category_slug)
                queryList = Trouser.objects.filter(category=sub_category).prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')
            else:
                queryList = Trouser.objects.all().prefetch_related('variant', 'variant__trouser_variant_meta', 'variant__trouser_variant_images')
        return queryList

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