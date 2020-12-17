import json
from math import ceil

from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.safestring import mark_safe

import webcolors

from cart.cart import Cart
from menu.models import Menu
from shop.models import TrouserVariant

register = template.Library()

# from django.http import HttpResponseRedirect
# from django.core.mail import send_mail
# from django.contrib import messages
# from django.http import HttpResponseRedirect

# from blog.models import Post
# import logging
# logger = logging.getLogger(__name__)

# @register.filter
# def model_name(obj):
#     try:
#         return obj._meta.model_name
#     except AttributeError:
#         return None

@register.filter
def form_url(obj):
    tempr = obj.get_ancestors(include_self=True)
    args = [temp.slug for temp in tempr]
    return reverse('menu:trouser_by_category', args=args)

@register.filter
def color_name(hexcode):
    return webcolors.hex_to_name(hexcode).title()

@register.filter
def removeslash(string):
    substring = string.split("/")
    return "/".join(substring[:-2])

@register.filter
def jsonify(cart):
    return mark_safe(json.dumps(cart))

@register.filter
def jsonnn(obj):
    return mark_safe(serialize('json', obj))

@register.filter
def currency(naira):
    if naira:
        naira = round(float(naira), 2)
        return mark_safe("NGN {}{}".format(intcomma(int(naira)), ("%0.2f" % naira)[-3:]))

# @register.filter(is_safe=False)
# def times(number):
#     return range(ceil(number))

# @register.filter(is_safe=False)
# def divide(value, arg):
#     """Divide the arg to the value."""
#     try:
#         return int(value) / int(arg)
#     except (ValueError, TypeError):
#         try:
#             return value / arg
#         except Exception:
#             return ''

@register.filter(is_safe=False)
def addfloatt(value, arg):
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''

@register.simple_tag
def settings(name):
    print("here")
    print(getattr(settings, "DEBUG", ""))
    return getattr(settings, name, "")
    
@register.inclusion_tag('tags/_menu.html', takes_context=True)
def menu(context):
    menus = Menu.objects.filter(is_active=True)
    request = context['request']
    return {'menus': menus, 'request': request}

@register.inclusion_tag('tags/_cartlist.html', takes_context=True)
def cartlist(context):
    request = context['request']
    cart = Cart(request)
    carttmp = request.session.get('cart')

    trousers_dict = {}

    trouser_ids = carttmp.keys()
    trousers = TrouserVariant.objects.filter(id__in=trouser_ids).prefetch_related('trouser_variant_meta')
    
    for trouser in trousers:
        carttmp[str(trouser.id)]['trouser'] = trouser.__str__()
        carttmp[str(trouser.id)]['id'] = trouser.id
    
    for x, item in enumerate(cart):
        trouser = item['trouser']
        for i, size in enumerate(item['size']):
            quantity = item['quantity'][i]
            total_price = item['total_price'][i]
            trousers_dict[size + str(x)] = {'name': trouser, 'size': size, 'quantity': quantity, 'total_price': total_price}  
    print(item)
    return {'trousers': trousers_dict, 'request': request}

# @register.inclusion_tag('tags/_contact_us.html')
# def contact_us():
#     return {'form': EmailPostForm()}

# @register.inclusion_tag('tags/_side_bar.html')
# def side_bar():
#     posts = Post.objects.published()[:5]
#     return {'posts': posts}

# @register.inclusion_tag('tags/_subscriber.html')
# def subscribe():
#     return {'form': SubscribeForm()}    

# @register.inclusion_tag('tags/_carousel.html')
# def carousel(id):
#     post = Post.objects.get(id=id)
#     return{'post': post}
