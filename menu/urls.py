from django.conf.urls import url
from django.urls import path, re_path

from shop.views import ProductByCategory

app_name = 'menu'
urlpatterns = [
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?$', ProductByCategory.as_view(), name='product_by_category'),
]