from django.urls import include, path, re_path
from django.views.generic.base import TemplateView, View

from shop.views import (HomeView, TrouserDetail, TrouserDetailAPI,
                        ProductListing, TrouserSearchList, BestSellerListing, NewArrivalsListing)

app_name = 'shop'

urlpatterns = [
    #index

    path('', HomeView.as_view(), name='shop-index'),
    
    #api

    re_path(r'^api/products/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?$', ProductListing.as_view(), name='listing'),
    path('api/trouser/<str:slug>/detail/', TrouserDetailAPI.as_view(), name='api-detail'),
    path('api/trouser/items/search/', TrouserSearchList.as_view(), name='api-search'),
    path('api/products/index/new-arrivals/items/', NewArrivalsListing.as_view(), name='api-new-arrivals'),
    path('api/products/index/best-sellers/items/', BestSellerListing.as_view(), name='api-best-sellers'),

    #others

    path('<str:slug>/', TrouserDetail.as_view(), name='detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='collection-detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='sub-collection-detail'),
    
]