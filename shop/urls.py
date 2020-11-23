from django.urls import path, include, re_path
from django.views.generic.base import View, TemplateView
from shop.views import HomeView, TrouserListing, TrouserDetail, TrouserDetailAPI

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='shop-index'),

    re_path(r'^api/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?$', TrouserListing.as_view(), name='listing'),
    path('api/trouser/<str:slug>/detail/', TrouserDetailAPI.as_view(), name='api-detail'),

    path('<str:slug>/', TrouserDetail.as_view(), name='detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='collection-detail'),
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?items/(?:(?P<slug>[-\w]+)/)?$', TrouserDetail.as_view(), name='sub-collection-detail'),
    
]