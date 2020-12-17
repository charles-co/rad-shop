from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from accounts.tokens import default_token_generator

# Create your models here.
DEFAULT_ACTIVATION_DAYS = getattr(settings, 'PASSWORD_RESET_TIMEOUT_DAYS', 3)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and password.
        '''
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, blank=False)

    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return self.first_name + " " + self.last_name
        else:
            if self.last_name:
                return self.last_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
              ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
              )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email=email) | 
                    Q(user__email=email)
                ).filter(
                    activated=False
                )


class EmailActivation(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emails")
    email           = models.EmailField()
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=3) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        user = self.user
        user.is_active = True
        user.save()
        self.activated = True
        self.save()


    def send_activation(self):
        if not self.activated and not self.forced_expired:
            uid = urlsafe_base64_encode(force_bytes(self.pk))
            token = default_token_generator.make_token(self)
            base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
            key_path = reverse("accounts:email-activate", kwargs={'uid64': uid, 'token': token}) # use reverse
            path = "{base}{path}".format(base=base_url, path=key_path)
            context = {
                'path': path,
                'email': self.email,
            }
            txt_ = get_template("registration/emails/verify.txt").render(context)
            html_ = get_template("registration/emails/verify.html").render(context)
            subject = '1-Click Email Verification'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.email]
            sent_mail = send_mail(
                        subject,
                        txt_,
                        from_email,
                        recipient_list,
                        html_message=html_,
                        fail_silently=False,
                )
            self.timestamp = timezone.now()
            self.save()
            return sent_mail
        return False

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated_at     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email