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
    name = forms.CharField(label='FullName', max_length=50, required=True, help_text='Shipping to? Who is it for?')
    phone = forms.CharField(label='Mobile No.', required=True, help_text='eg. +234XXXXXXXXXX')
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
