from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, related_name="addresses", on_delete=models.CASCADE)
    name            = models.CharField('Fullname', max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname        = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    phone           = PhoneNumberField(null=True, blank=True, help_text='eg. +234XXXXXXXXXX')
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='Nigeria', editable=False)
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=6)
    default         = models.BooleanField('Set as default address', default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['billing_profile', 'address_line_1', 'city', 'state',], name='unique address')
        ]

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line_1)

    def save(self, *args, **kwargs):
        if self.default:
            temp = Address.objects.filter(billing_profile=self.billing_profile, default=True).update(default=False)
        else:
            temp =  Address.objects.filter(billing_profile=self.billing_profile)
            if temp.count() == 0:
                self.default = True
        if self.billing_profile and not self.name:
            self.name = self.billing_profile.user.get_full_name()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("accounts:address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name 
        if self.nickname:
            for_name = "{} | {},".format( self.nickname, for_name)
        return "{for_name} {line1}, {city}".format(
                for_name = for_name or "",
                line1 = self.address_line_1,
                city = self.city
            ) 

    def get_address(self):
        return "{for_name}\n{line1}\n{city}\n{state}, {postal}\n{country}{phone}".format(
                for_name = self.name or "",
                line1 = self.address_line_1,
                city = self.city,
                state = self.state,
                postal= self.postal_code,
                country = self.country,
                phone = ",\n" + str(self.phone) or ""
            )