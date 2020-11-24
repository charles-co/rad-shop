from django.conf.urls import url
from django.urls import path, re_path

from shop.views import TrouserByCategory

app_name = 'menu'
urlpatterns = [
    re_path(r'^categories/(?:(?P<first_slug>[-\w]+)/)?(?:(?P<second_slug>[-\w]+)/)?$', TrouserByCategory.as_view(), name='trouser_by_category'),
]