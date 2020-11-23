from django.urls import path, include, re_path
from django.views.generic.base import View, TemplateView
from accounts.views import SignUpView, AccountEmailActivateView, LoginView, AccountHomeView, UserDetailUpdateView, GuestRegisterView
from addresses.views import (
    AddressCreateView,
    AddressListView,
    AddressUpdateView,
    )
from django.contrib.auth.views import LogoutView


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('dashboard/', AccountHomeView.as_view(), name='account-home'),
    path('dashboard/details/', UserDetailUpdateView.as_view(), name='account-update'),
    path('email/activate/<str:uid64>/<str:token>/', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/', AddressUpdateView.as_view(), name='address-update'),
]