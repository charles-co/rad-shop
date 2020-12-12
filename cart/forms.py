import datetime
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from cart.validators import CCNumberValidator, CSCValidator, ExpiryDateValidator
from cart.widgets import TelephoneInput, ExpiryDateWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField
from crispy_forms.bootstrap import AppendedText, PrependedText
from . import utils


# __all__ = ['CardNumberField', 'CardExpiryField', 'SecurityCodeField']


class CardNumberField(forms.CharField):
    widget = TelephoneInput
    default_validators = [
        MinLengthValidator(16),
        MaxLengthValidator(19),
        CCNumberValidator(),
    ]

    def to_python(self, value):
        return utils.get_digits(super().to_python(value))

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'[-\d\s]*',
            'autocomplete': 'cc-number',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs


class CardExpiryField(forms.DateField):
    widget = ExpiryDateWidget
    input_formats = ['%m/%y', '%m/%Y']
    default_validators = [ExpiryDateValidator()]

    def prepare_value(self, value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.strftime('%m/%y')
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, datetime.date):
            value = utils.expiry_date(value.year, value.month)
        return value

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d+/\d+',
            'placeholder': 'MM/YY',
            'autocomplete': 'cc-exp',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs


class SecurityCodeField(forms.CharField):
    widget = TelephoneInput
    default_validators = [CSCValidator()]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'pattern': r'\d*',
            'autocomplete': 'cc-csc',
            'autocorrect': 'off',
            'spellcheck': 'off',
            'autocapitalize': 'off',
        })
        return attrs

class PaymentForm(forms.Form):
    cc_number = CardNumberField(max_length=19, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    cc_expiry = CardExpiryField()
    cc_code = SecurityCodeField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV'}), help_text="3 or 4 digits usually found on the signature strip")
    cc_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}), max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
                AppendedText('cc_number', '<i class="fab fa-money-check"></i>', active=True,css_class=""),
                Div(
                    Div(
                        AppendedText('cc_expiry', '<i class="fas fa-calendar-alt"></i>', active=True,css_class=""),
                        # AppendedText('cc_code', '<i class="far fa-credit-card"></i>', active=True,css_class=""),
                        css_class="col-5"
                    ),
                    Div(
                        # AppendedText('cc_expiry', '<i class="fas fa-calendar-alt"></i>', active=True,css_class=""),
                        AppendedText('cc_code', '<i class="far fa-credit-card"></i>', active=True,css_class=""),
                        css_class="col-5"
                    ),
                    css_class="row justify-content-between no-gutters"
                ),
                AppendedText('cc_name', '<i class="fas fa-user"></i>', active=True,css_class=""),
                ButtonHolder(
                    Submit('submit', 'Proceed', css_class="btn-success btn-block py-2")
                ),
                
            )