from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    """
    User-related CRUD form
    """
    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            'phone',
            #'billing_profile',
            'address_type',
            'address_line_1',
            # 'address_line_2',
            'city',
            'state',
            'postal_code',
            'default'
        ]




class AddressCheckoutForm(forms.ModelForm):
    """
    User-related checkout address create form
    """
    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            'phone',
            #'billing_profile',
            'address_type',
            'address_line_1',
            # 'address_line_2',
            'city',
            'state',
            'postal_code'
        ]
