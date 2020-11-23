from django.shortcuts import render
import json
from decimal import Decimal
from templatetags.extras import currency
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Trouser, TrouserVariant
from .cart import Cart
from sorl.thumbnail import get_thumbnail
from django.http import JsonResponse
from .forms import CartAddProductForm
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressCheckoutForm
from orders.models import Order, OrderItem
from billing.models import BillingProfile
from addresses.models import Address

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
        
@require_POST
def cart_add(request):
    data = json.loads(request.body)
    cart = Cart(request)  
    id = data['trouser_id']
    size = data['size']
    update = data['update']
    quantity = data['quantity']
    trouser = get_object_or_404(TrouserVariant, id=id)
    if not update:
        cart.add(trouser=trouser, size=size, quantity=1, update_quantity=False)
    else:
        cart.add(trouser=trouser, size=size, quantity=quantity, update_quantity=True)
    return JsonResponse({'status': 'Ok', 'total_items': str(cart.__len__())})

def cart_remove(request):
    data = json.loads(request.body) 
    id = data['trouser_id']
    size = data['size']
    cart = Cart(request)
    trouser = get_object_or_404(TrouserVariant, id=id)
    cart.remove(trouser, size)
    return JsonResponse({'status': 'Ok', 'total_items': str(cart.__len__())})

def cart_detail(request):
    cart = Cart(request)
    trousersString = ''
    carttmp = request.session.get('cart')
    trouser_ids = carttmp.keys()
    trousers = TrouserVariant.objects.filter(id__in=trouser_ids).prefetch_related('trouser_variant_meta', 'trouser_variant_images')
    for trouser in trousers:
        carttmp[str(trouser.id)]['trouser'] = trouser
    for item in cart:
        trouser=item['trouser']
        for i, size in enumerate(item['size']):
            im = get_thumbnail(trouser.trouser_variant_images.first().file, '120x160', crop='center', quality=99)
            stock = trouser.trouser_variant_meta.get(size=size).stock
            quantity = item['quantity'][i]
            total_price = item['total_price'][i]
            key = str(trouser.id) + str(size)
            b = "{'id': '%s','name': '%s', 'price': '%s', 'size': '%s', 'quantity': '%s', 'total_price': '%s', 'url': '%s','image_url': '%s','stock': '%s', 'key': '%s'}," % (trouser.id, trouser.trouser.name, trouser.price, size, quantity, total_price, trouser.trouser.get_absolute_url(), im.url, stock, key)
            trousersString = trousersString + b
    return render(request, 'cart/detail.html', {'cart': cart, 'trousersString': trousersString})


def checkout_home(request):
    cart = Cart(request)
    order_obj = None

    if cart.get_length() == 0:
        return redirect("shop:collections")  

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()

    shipping_address_id = request.session.get("shipping_address_id", None)
    order_id = request.session.get("order_id", None)
    billing_profile = BillingProfile.objects.new_or_get(request)
    # print(billing_profile)
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
                print(shipping_address_id)
        else:
            if address_qs:
                address = address_qs.first()
                shipping_address_id = request.session.get("shipping_address_id", address.id)
                address_form = AddressCheckoutForm(instance=address)
    
        trousersString = ''
        order_obj = Order.objects.new_or_get(billing_profile, order_id=order_id)
        request.session["order_id"] = order_obj.id
        if shipping_address_id:
            print("goot here bruh")
            address_temp = Address.objects.get(id=shipping_address_id)
            order_obj.shipping_address = address_temp
            print(order_obj.shipping_address)
            order_obj.save()
            try:
                del request.session["shipping_address_id"]
            except KeyError:
                pass

    if request.method == "POST":
        "check that order is done"
        for item in cart:
            if len(item['size']) == 1:
                OrderItem.objects.create(order=order,
                trouser=item['trouser'],
                price=item['price'],
                quantity=item['quantity'],
                size=item['size'])
            else:
                for i,size in enumerate(item['size']):
                    OrderItem.objects.create(order=order,
                    trouser=item['trouser'],
                    price=item['price'],
                    quantity=item['quantity'][i],
                    size=size)
        # clear the cart
        cart.clear()
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "address": address,
        "shipping_address_id": shipping_address_id,
        "address_form": address_form,
    }
    return render(request, "cart/checkout.html", context)