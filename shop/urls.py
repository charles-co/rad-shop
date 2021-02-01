from django.urls import include, path, re_path
from django.views.generic.base import TemplateView, View

from rest_framework import routers

from shop.views import (HomeView, ProductDetail, ProductByCategory)

from shop.api.views import (getColors, getIndexSlideshow, ProductDetailAPI, ProductViewSet, 
                        TrouserViewSet, WavecapViewSet,)
app_name = 'shop'

router = routers.DefaultRouter()
router.register(r'all-products', ProductViewSet, basename='products')
router.register(r'trousers', TrouserViewSet, basename='trousers')
router.register(r'wavecaps', WavecapViewSet, basename='wavecaps')

urlpatterns = [
    #index

    path('', HomeView.as_view(), name='shop-index'),
    
    #api
    path('api/', include((router.urls, 'shop'))),
    path('api/colors/', getColors, name='colors'),
    path('api/index/slideshow/', getIndexSlideshow, name='index-slideshow'),
    # path('api/trouser/items/search/', TrouserSearchList.as_view(), name='api-search'),

    #others
    path('<str:product_slug>/<str:slug>/', ProductDetail.as_view(), name='detail'),
    # re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?items/(?:(?P<product_slug>[-\w]+)/)?(?:(?P<slug>[-\w]+)/)?$', ProductDetail.as_view(), name='collection-detail'),
    # re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?items/(?:(?P<product_slug>[-\w]+)/)?(?:(?P<slug>[-\w]+)/)?$', ProductDetail.as_view(), name='sub-collection-detail'),
]