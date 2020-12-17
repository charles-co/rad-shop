from django.conf import settings
from django.db import models
from django.urls import reverse

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

# Create your models here.
class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.filter(id=guest_email_id)
            if not guest_email_obj.exists():
                del request.session["guest_email_id"]
            else:
                guest_email_obj = guest_email_obj.first().email
                obj, created = self.model.objects.get_or_create(email=guest_email_obj, user=None)
                # print(obj, created)
        else:
            pass
        return obj

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update_at    = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    # customer_id in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email