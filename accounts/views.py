from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.views.generic import (CreateView, DetailView, FormView,
                                  TemplateView, UpdateView, View)
from django.views.generic.edit import FormMixin

from accounts.models import EmailActivation
from accounts.tasks import EmailVerification
from accounts.tokens import default_token_generator
from rad.mixins import NextUrlMixin, RequestFormAttachMixin

from .forms import (GuestForm, LoginForm, ReactivateEmailForm, SignUpForm,
                    UserDetailChangeForm)

# Create your views here.
use_celery = getattr(settings, 'PYTHON_ANYWHERE', False)
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        request = self.request
        messages.info(request, "A confirmation main has been sent to you, please chack your mail to activate your account.")
        return super(SignUpView, self).form_valid(form)

    
class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = reverse_lazy('accounts:signup')

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

class AccountEmailActivateView(FormMixin, View):
    success_url = reverse_lazy('accounts:login')
    form_class = ReactivateEmailForm
    uid64 = None
    token = None
    def get(self, request, *args, **kwargs):
        try:
            self.uid64 = self.kwargs['uid64']
            self.token = self.kwargs['token']
            uid = force_text(urlsafe_base64_decode(self.uid64))
            email = EmailActivation.objects.get(pk=uid)
        except (TypeError, KeyError, ValueError, OverflowError, EmailActivation.DoesNotExist):
            email = None

        if email and default_token_generator.check_token(email, self.token):
            email.activate()
            messages.success(request, "Your email has been confirmed. Please login.")
            return redirect("accounts:login")
        else:
            if email and email.activated:
                reset_link = reverse("password_reset")
                msg = """Your email has already been confirmed
                Do you need to <a class="text-primary" href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.info(request, mark_safe(msg))
                return redirect("accounts:login")
            else:
                if self.token and self.uid64:
                    self.error = True
                else:
                    self.error = False

        context = {'form': self.get_form(), 'error': self.error}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.info(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.get(email=email)
        if not use_celery:
            EmailVerification.delay(obj.id, msg)
        else:
            obj.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "error": self.error }
        return render(self.request, 'registration/activation-error.html', context)

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = reverse_lazy('shop:shop-index')
    template_name = 'accounts/login.html'
    default_next = 'shop:shop-index'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signupform"] = SignUpForm
        request = self.request
        return context

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("accounts:account-home")