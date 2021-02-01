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

import webcolors

from contents.models import ShopIndex
from menu.models import Menu
from shop.models import Image, Product, Trouser, TrouserVariant, Wavecap, WavecapVariant

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class HomeView(TemplateView):
    template_name = "shop/index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.home = ShopIndex.objects.all().first()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home'] = self.home
        return context

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

class ProductDetail(TemplateView):
    template_name = 'shop/item_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['product_slug'] = self.kwargs['product_slug']
        return context

def handler404(request, exception):
    return render(request, 'error.html', {'error': '404', 'error_message': '404, Page Not Found'}, status=404)

def handler400(request, exception):
    return render(request, 'error.html', {'error': '400', 'error_message': '400, Bad Request'}, status=400)

def handler500(request):
    return render(request, 'error.html', {'error': '500', 'error_message': '500, Internal Server Error'}, status=500)