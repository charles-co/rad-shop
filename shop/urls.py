from django.urls import include, path, re_path
from django.views.generic.base import TemplateView, View

from shop.views import (HomeView, TrouserDetail, TrouserDetailAPI,
                        TrouserListing, TrouserSearchList, BestSellerListing, NewArrivalsListing)

app_name = 'shop'

urlpatterns = [
    #index

    path('', HomeView.as_view(), name='shop-index'),
    
    #api

    re_path(r'^api/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?$', TrouserListing.as_view(), name='listing'),
    path('api/trouser/<str:slug>/detail/', TrouserDetailAPI.as_view(), name='api-detail'),
    path('api/trouser/items/search/', TrouserSearchList.as_view(), name='api-search'),
    path('api/trouser/index/new-arrivals/items/', NewArrivalsListing.as_view(), name='api-new-arrivals'),
    path('api/trouser/index/best-sellers/items/', BestSellerListing.as_view(), name='api-best-sellers'),

    #others

    path('<str:slug>/', TrouserDetail.as_view(), name='detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='collection-detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='sub-collection-detail'),
    
]