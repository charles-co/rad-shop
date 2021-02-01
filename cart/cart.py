import datetime
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
        keys = list(self.cart.keys())
        for key in keys:
            for item in self.cart[key]:
                temp = {}
                obj = {}
                self.cart[key][item]['price'] = float(self.cart[key][item]['price'])
                self.cart[key][item]['total_price'] = []
                for i, x  in enumerate(self.cart[key][item]['size']):
                    self.cart[key][item]['total_price'].append(self.cart[key][item]['price'] * self.cart[key][item]['quantity'][i])
                temp[item] = self.cart[key][item]
                obj[key] = temp
                yield obj
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        total = 0
        keys = list(self.cart.keys())
        for key in keys:
            total += sum([sum(x['quantity']) for x in self.cart[key].values()])
        return total
    
    def add(self, product, _type, size=None, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)    
        size = str(size)
        if _type not in self.cart:
            product_obj = {_type:{product_id: {
                                'size': [str(size)], 
                                'quantity': [0], 
                                'price': str(product.price),
                                'time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                            },
                        },
                    }
            self.cart.update(product_obj)
        elif _type in self.cart and product_id not in self.cart[_type].keys():
            self.cart[_type][product_id] = {'size': [str(size)], 
                                            'quantity': [0], 
                                            'price': str(product.price),
                                            'time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                                        }
        elif _type in self.cart and product_id in self.cart[_type].keys() and size not in self.cart[_type][product_id]['size']:
            self.cart[_type][product_id]['size'].append(str(size))
            self.cart[_type][product_id]['quantity'].append(0)
        else:
            print("bad ! badder !! baddest !!!")

        index = self.cart[_type][product_id]['size'].index(size)
   
        if update_quantity:
            self.cart[_type][product_id]['quantity'][index] = quantity
        else:
            self.cart[_type][product_id]['quantity'][index] += quantity
        self.save()
    
    def remove(self, product, _type, size=None):
        """
        Remove a product from the cart.
        """
        size = str(size)
        product_id = str(product.id)
        if _type in self.cart and product_id in self.cart[_type].keys() and size in self.cart[_type][product_id]["size"]:
            if len(self.cart[_type][product_id]["size"]) > 1:
                index = self.cart[_type][product_id]['size'].index(size)
                quantity = self.cart[_type][product_id]['quantity'][index]
                self.cart[_type][product_id]['size'].remove(size) 
                self.cart[_type][product_id]['quantity'].remove(quantity)
                self.save()
            else:
                del self.cart[_type][product_id]
                self.save()
    
    def get_total_price(self):
        
        total = 0
        keys = list(self.cart.keys())
        for key in keys:
            total += sum(Decimal(x['price']) * sum(x['quantity']) for x in self.cart[key].values())
        return total
    
    def get_length(self):
        return str(self.__len__())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True