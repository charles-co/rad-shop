from django.conf.urls import url
from django.urls import path

from accounts.views import guestemailedit
from addresses.views import (checkout_address_create_view,
                             checkout_address_reuse_view, guestaddressedit)
from cart.views import cart_add, cart_detail, cart_remove, checkout_home, cart_remove_all, Payment

app_name='cart'
urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/', cart_add, name='cart-add'),
    path('remove/', cart_remove, name='cart-remove'),
    path('remove-all/', cart_remove_all, name='cart-remove-all'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('checkout/guest/address/edit/', guestaddressedit, name='guest_address_edit'),
    path('checkout/guest/email/edit/', guestemailedit, name='guest_email_edit'),
    path('checkout/payment/', Payment.as_view(), name='payment'),
]
