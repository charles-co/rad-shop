from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText
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
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset(
                        'Personal Info',
                        Field('nickname', css_class="rounded-0"),
                        Field('name', css_class="rounded-0"),
                        Field('phone', css_class="rounded-0"),
                        css_class="p-4 mb-4"
                    ),
                    css_class="col-md-6",
                ),
                Div(
                    Fieldset(
                        'Address Info',
                        Field('address_type', css_class="rounded-0"),
                        Field('address_line_1', css_class="rounded-0"),
                        Field('city', css_class="rounded-0"),
                        Field('state', css_class="rounded-0"),
                        Field('postal_code', css_class="rounded-0"),
                        Div(
                            Field('default', css_class="rounded-0 custom-control-input"),
                            css_class="custom-control custom-switch",
                        ),
                        css_class="p-4 mb-3",

                    ),
                    css_class="col-md-6",
                ),
                ButtonHolder( 
                    Submit('submit', 'Save', css_class="btn btn-primary btn-md rounded-0 btn-block py-2"),
                    css_class="w-100 col-12",
                ),
                css_class="row mb-3"
            )
        )
        super(AddressForm, self).__init__(*args, **kwargs)




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
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
                Div(
                    Div(
                        Fieldset(
                            'Personal Info',
                            Field('nickname', css_class="rounded-0"),
                            Field('name', css_class="rounded-0"),
                            Field('phone', css_class="rounded-0"),
                            css_class="p-4 mb-4"
                        ),
                        css_class="col-md-6",
                    ),
                    Div(
                        Fieldset(
                            'Address Info',
                            Field('address_type', css_class="rounded-0"),
                            Field('address_line_1', css_class="rounded-0"),
                            Field('city', css_class="rounded-0"),
                            Field('state', css_class="rounded-0"),
                            Field('postal_code', css_class="rounded-0"),
                            css_class="p-4 mb-3"
                        ),
                        css_class="col-md-6",
                    ),
                    ButtonHolder( 
                        Submit('submit', 'Proceed', css_class="btn btn-primary btn-md rounded-0 btn-block py-2"),
                        css_class="w-100",
                    ),
                    css_class="row"
                )
            )
        super(AddressCheckoutForm, self).__init__(*args, **kwargs)
