from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView, View

from accounts.views import (AccountEmailActivateView, AccountHomeView,
                            GuestRegisterView, LoginView, SignUpView,
                            UserDetailUpdateView)
from addresses.views import (AddressCreateView, AddressListView,
                             AddressUpdateView)

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