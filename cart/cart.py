import json
from collections import OrderedDict
from decimal import Decimal

from django.conf import settings

from shop.models import Trouser, TrouserVariant

class Cart(object):

    def __init__(self, request):    
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        # trouser_ids = self.cart.keys()
        # # get the trouser objects and add them to the cart
        # trousers = TrouserVariant.objects.filter(id__in=trouser_ids).prefetch_related('trouser_variant_meta', 'trouser_variant_images')
        # for trouser in trousers:
        #     self.cart[str(trouser.id)]['trouser'] = trouser
        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = []
            for i, x  in enumerate(item['size']):
                item['total_price'].append(item['price'] * item['quantity'][i])
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(sum(item['quantity']) for item in self.cart.values())
    
    def add(self, trouser, size, quantity=1, update_quantity=False):
        """
        Add a trouser to the cart or update its quantity.
        """
        trouser_id = str(trouser.id)      
        size = str(size)
        if trouser_id not in self.cart:
            temp = {trouser_id: {'size': [str(size)], 'quantity': [0], 'price': str(trouser.price)}}
            temp.update(self.cart)
            self.cart = temp
        elif trouser_id in self.cart and str(size) not in self.cart[trouser_id]["size"]:
            self.cart[trouser_id]['size'].append(str(size))
            self.cart[trouser_id]['quantity'].append(0)
            
        index = self.cart[trouser_id]['size'].index(size)
   
        if update_quantity:
            self.cart[trouser_id]['quantity'][index] = quantity
        else:
            self.cart[trouser_id]['quantity'][index] += quantity
        self.save()
    
    def remove(self, trouser, size):
        """
        Remove a trouser from the cart.
        """
        size = str(size)
        trouser_id = str(trouser.id)
        if trouser_id in self.cart and size in self.cart[trouser_id]["size"]:
            if len(self.cart[trouser_id]["size"]) > 1:
                index = self.cart[trouser_id]['size'].index(size)
                quantity = self.cart[trouser_id]['quantity'][index]
                self.cart[trouser_id]['size'].remove(size) 
                self.cart[trouser_id]['quantity'].remove(quantity)
                self.save()
            else:
                del self.cart[trouser_id]
                self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * sum(item['quantity']) for item in self.cart.values())
    
    def get_length(self):
        return self.__len__()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True