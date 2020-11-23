from django import forms
from django.core.mail import send_mail, send_mass_mail
from pagedown.widgets import AdminPagedownWidget
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout
from shop.models import Trouser
from crispy_forms.helper import FormHelper
# from crispy_forms import css_id
from crispy_forms.bootstrap import InlineField
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Div
from pagedown.widgets import AdminPagedownWidget
from tinymce.widgets import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class TrouserForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCEWidget(attrs={'requred': False, 'cols': 40, 'rows': 20}))
    class Meta:
        model = Trouser
        fields = "__all__"

