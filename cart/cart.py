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
        # product_ids = self.cart.keys()
        # # get the product objects and add them to the cart
        # products = TrouserVariant.objects.filter(id__in=product_ids).prefetch_related('product_variant_meta', 'product_variant_images')
        # for product in products:
        #     self.cart[str(product.id)]['product'] = product
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
    
    def add(self, product, size=None, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)      
        size = str(size)
        if product_id not in self.cart:
            temp = {product_id: {'size': [str(size)], 'quantity': [0], 'price': str(product.price)}}
            temp.update(self.cart)
            self.cart = temp
        elif product_id in self.cart and str(size) not in self.cart[product_id]["size"]:
            self.cart[product_id]['size'].append(str(size))
            self.cart[product_id]['quantity'].append(0)
            
        index = self.cart[product_id]['size'].index(size)
   
        if update_quantity:
            self.cart[product_id]['quantity'][index] = quantity
        else:
            self.cart[product_id]['quantity'][index] += quantity
        self.save()
    
    def remove(self, product, size):
        """
        Remove a product from the cart.
        """
        size = str(size)
        product_id = str(product.id)
        if product_id in self.cart and size in self.cart[product_id]["size"]:
            if len(self.cart[product_id]["size"]) > 1:
                index = self.cart[product_id]['size'].index(size)
                quantity = self.cart[product_id]['quantity'][index]
                self.cart[product_id]['size'].remove(size) 
                self.cart[product_id]['quantity'].remove(quantity)
                self.save()
            else:
                del self.cart[product_id]
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