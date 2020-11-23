from django.conf.urls import url
from django.urls import path
from cart.views import cart_detail, cart_add, cart_remove, checkout_home
from addresses.views import checkout_address_create_view, checkout_address_reuse_view, guestaddressedit

app_name='cart'
urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/', cart_add, name='cart-add'),
    path('remove/', cart_remove, name='cart-remove'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('checkout/guest/address/edit/', guestaddressedit, name='guest_address_edit'),
]
