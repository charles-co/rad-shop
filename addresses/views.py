from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import is_safe_url, url_has_allowed_host_and_scheme
from django.views.generic import CreateView, ListView, UpdateView

from billing.models import BillingProfile
from rad.mixins import NextUrlMixin, RequestFormAttachMixin

from .forms import AddressCheckoutForm, AddressForm
from .models import Address

# CRUD create update retrieve delete




class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'addresses/list.html'

    def get_queryset(self):
        request = self.request
        billing_profile = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile).order_by("-default")

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = reverse_lazy('accounts:addresses')
    default_next = 'accounts:addresses'

    def form_valid(self, form):
        next = self.request.GET.get('next')
        try:
            form.save()
            if next:
                return redirect(next)
        except(IntegrityError):
            messages.error(request, "Address already exist !")
            return redirect("accounts:addresses")
        return super(AddressUpdateView, self).form_valid(form)

    
    def get_queryset(self):
        request = self.request
        billing_profile = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)

def guestaddressedit(request):
    if request.method == "POST":
        id = request.POST.get('address-id')
        next = request.POST.get('next')
        address = Address.objects.filter(id=id).first()
        form =  AddressCheckoutForm(request.POST, instance=address)
        if form.is_valid:
            try:
                form.save()
                if url_has_allowed_host_and_scheme(next, request.get_host()):
                    return redirect(next)
            except(IntegrityError):
                messages.error(request, "Address already exist !")
                return redirect("cart:checkout")
        else:
            messages.error(request, "Edit Unsuccessful")
            return redirect('cart:checkout')

class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = reverse_lazy('accounts:addresses')

    def form_valid(self, form):
        request = self.request
        billing_profile = BillingProfile.objects.new_or_get(request)
        instance = form.save(commit=False)
        instance.billing_profile = billing_profile
        next = self.request.GET.get('next', None)
        try:
            instance.save()
            if next:
                return redirect(next)
        except(IntegrityError):
            messages.error(request, "Address already exist !")
            return redirect("accounts:addresses")
        return super(AddressCreateView, self).form_valid(form)

def checkout_address_create_view(request):
    form = AddressCheckoutForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
        else:
            print("Error here")
            return redirect("cart:checkout")

        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("cart:checkout")

def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:

                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout") 