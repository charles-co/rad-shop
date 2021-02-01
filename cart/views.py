import json
from decimal import Decimal

from django.apps import AppConfig, apps
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import (CreateView, DetailView, FormView,
                                  TemplateView, UpdateView, View)
                                  
from sorl.thumbnail import get_thumbnail

from accounts.forms import GuestForm, LoginForm
from addresses.forms import AddressCheckoutForm
from addresses.models import Address
from billing.models import BillingProfile
from accounts.models import GuestEmail
from orders.models import Order, OrderItem
from shop.models import Trouser, TrouserVariant
from templatetags.extras import currency

from cart.cart import Cart
from cart.forms import PaymentForm

@require_POST
def cart_add(request):
    data = json.loads(request.body)
    cart = Cart(request)  
    _id = data['product_id']
    size = data['size'] or None
    update = data['update']
    quantity = data['quantity']
    _type = data['type']
    __type = data['type'] + "variant"
    Klass = apps.get_model('shop', __type)
    product = get_object_or_404(Klass, id=_id)
    if not update:
        cart.add(product=product, _type=_type, size=size, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, _type=_type, size=size, quantity=quantity, update_quantity=True)
    return JsonResponse({'status': 'Ok', 'total_items': cart.get_length()})

@require_POST
def cart_remove(request):
    data = json.loads(request.body) 
    cart = Cart(request)
    _id = data['product_id']
    size = data['size']
    _type = data['type']
    __type = data['type'] + "variant"
    Klass = apps.get_model('shop', __type)
    product = get_object_or_404(Klass, id=_id)
    cart.remove(product, _type, size)
    return JsonResponse({'status': 'Ok', 'total_items': cart.get_length()})

@require_POST
def cart_remove_all(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'status': 'Ok', 'total_items': cart.get_length()})

@require_GET
def cart_detail(request):
    cart_obj = Cart(request)
    products_string = []
    cart = {}
    for item in cart_obj:
        for key in item.keys():
            try:
                cart[key] = {**cart[key], **item[key]}
            except KeyError:
                cart[key] = item[key]
    products = cart.keys()
    for product in products:
        __type = product + "variant"
        product_ids = cart[product].keys()
        Klass = apps.get_model('shop', __type)
        product_obj = Klass.objects.filter(id__in=product_ids).prefetch_related('images')
        for item in product_obj:
            cart[product][str(item.id)]['obj'] = item
        for item in cart[product]:
            obj = cart[product][item]['obj']
            for i, size in enumerate(cart[product][item]['size']):
                im = get_thumbnail(obj.images.first().file, '120x160', quality=99)
                try:
                    stock = obj.metas.get(size=size).stock
                except:
                    stock = obj.stock
                quantity = cart[product][item]['quantity'][i]
                time = cart[product][item]['time']
                total_price = cart[product][item]['total_price'][i]
                unique_key = str(product) + str(obj.id) + str(size)
                result = {'id': obj.id,
                        'name': obj.__str__(), 
                        'price': obj.price, 
                        'size': size, 
                        'quantity': quantity, 
                        'total_price': total_price, 
                        'url': obj.get_absolute_url(),
                        'image_url': im.url,
                        'stock': stock, 
                        'key': unique_key, 
                        'time': time}
                products_string.append(result)
    return JsonResponse({'cart': products_string, 'count': cart_obj.get_length(), 'total_price': cart_obj.get_total_price()})


def checkout_home(request):
    cart = Cart(request)
    order_obj = None

    if cart.get_length() == 0:
        messages.info(request, "No item in cart.")
        return redirect("menu:trouser_by_category", "collections")  
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)

    shipping_address_id = request.session.get("shipping_address_id", None)
    order_id = request.session.get("order_id", None)
    old_post = request.session.get("old_form_post", None)

    address_form = AddressCheckoutForm(initial=old_post)
    billing_profile = BillingProfile.objects.new_or_get(request)
    address_qs = None
    address = None

    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        if request.user.is_authenticated:
            if address_qs:
                if shipping_address_id:
                    address = address_qs.filter(id=shipping_address_id).first()
                else:
                    address = address_qs.filter(default=True).first()
                    if not address:
                        address = address_qs.first()
                shipping_address_id = request.session.get("shipping_address_id", address.id)
        else:
            if address_qs:
                try:
                    del request.session["old_form_post"]
                except KeyError:
                    pass
                address = address_qs.first()
                shipping_address_id = request.session.get("shipping_address_id", address.id)
                address_form = AddressCheckoutForm(instance=address)
                guest_form = GuestForm(request=request, initial={'email': billing_profile.email, })
    
        trousersString = ''
        order_obj = Order.objects.new_or_get(billing_profile, order_id=order_id)
        request.session["order_id"] = order_obj.id
        if shipping_address_id:
            address_temp = Address.objects.get(id=shipping_address_id)
            order_obj.shipping_address = address_temp
            # print(order_obj.shipping_address)
            order_obj.save()
            try:
                del request.session["shipping_address_id"]
            except KeyError:
                pass

    if request.method == "POST":
        "check that order is done"
        try:
            order_obj.orders.all().delete()
        except ObjectDoesNotExist:
            print("error")
        finally:
            trouser_temp = {}
            carttmp = request.session.get('cart')
            trouser_ids = carttmp.keys()
            trousers = TrouserVariant.objects.filter(id__in=trouser_ids).prefetch_related('trouser_variant_meta', 'trouser_variant_images')
            for trouser in trousers:
                trouser_temp[str(trouser.id)] = trouser
            for key, item in carttmp.items():
                if len(item['size']) == 1:
                    OrderItem.objects.create(order=order_obj,
                    trouser=trouser_temp[key],
                    price=item['price'],
                    quantity=item['quantity'][0],
                    size=item['size'][0],
                    billing_profile=billing_profile)
                else:
                    for i, size in enumerate(item['size']):
                        OrderItem.objects.create(order=order_obj,
                        trouser=trouser_temp[key],
                        price=item['price'],
                        quantity=item['quantity'][i],
                        size=size,
                        billing_profile=billing_profile)
            # clear the cart
            msg = "Order created successfully."
            messages.success(request, msg)
            return redirect('cart:payment')
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "address": address,
        "shipping_address_id": shipping_address_id,
    }
    return render(request, "cart/checkout.html", context)

class AjaxableResponseMixin(object):
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({"errors" : form.errors}, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.request.is_ajax():
            data = {
                'statuses': 'ok',
            }
            return JsonResponse(data)
        else:
            return response

class Payment(AjaxableResponseMixin, FormView):
    form_class = PaymentForm
    template_name = "cart/payment.html"

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request)
        order_id = request.session.get("order_id", None)
        self.order = Order.objects.filter(id=order_id).select_related('shipping_address', 'billing_profile').first()
        if request.method == "GET":
            if request.build_absolute_uri(reverse("cart:checkout")) != request.META.get('HTTP_REFERER'):
                return redirect("cart:checkout")
        elif request.method == "POST":
            data = json.loads(request.body)
            form = PaymentForm(data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_info"] = self.order
        context["cart"] = self.cart
        return context
    




