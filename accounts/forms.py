from django import forms
from django.contrib.auth import (authenticate, get_user_model, login,
                                 password_validation)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText, PrependedAppendedText

from accounts.models import EmailActivation, GuestEmail

User = get_user_model()

# from .models import EmailActivation, GuestEmail


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email) 
        if not qs.exists():
            register_link = reverse("accounts:signup")
            msg = """This email does not exists, would you like to <a href="{link}">register</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password confirmation'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('email',) #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserDetailChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class LoginForm(forms.Form):
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
                PrependedText('email', '<i class="fas fa-user-circle text-info"></i>', active=True, css_class="rounded-0"),
                PrependedAppendedText('password', '<i class="fas fa-key text-info"></i>', '<button type="button" @click="passwordshow($event)" class="btn btn-sm bg-transparent remove-outline p-0"><i class="fas fa-eye-slash text-info"></i></button>', active=True, css_class="rounded-0 border-right-0"),
            )
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email  = data.get("email")
        password  = data.get("password")
        qs = User.objects.filter(email=email).first()
        if qs:
            # user email is registered, check active/
            if not(qs.is_active):
                ## not active, check email activation
                link = reverse("accounts:resend-activation")
                reconfirm_msg = """Go to <a class="text-primary" href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        return data

class SignUpForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    first_name = forms.CharField(label='First Name', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label='Email Address', max_length=255, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
                        Field('first_name', css_class="rounded-0"),
                        Field('last_name', css_class="rounded-0"),
                        Field('email', css_class="rounded-0"),
                        Field('password1', css_class="rounded-0"),
                        Field('password2', css_class="rounded-0"),
                        HTML("""<p class='small font-italic'>A verification mail will be sent to the specified email on form completion.</p>"""),
                    )
        super(SignUpForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False # send confirmation email via signals
        if commit:
            user.save()
        return user

class GuestForm(forms.ModelForm):
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
                PrependedText('email', '<i class="fas fa-user-circle text-info"></i>', active=True, css_class="rounded-0"),
            )
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            email = obj.email
            request = self.request
            dupl = GuestEmail.objects.filter(email=email)
            if not dupl.exists():
                obj.save()
            else:
                obj = dupl.first()
            request.session['guest_email_id'] = obj.id
        return obj



