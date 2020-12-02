from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from accounts.models import EmailActivation
from accounts.tokens import default_token_generator

@shared_task
def EmailVerification(id):
    email = EmailActivation.objects.get(id=id)
    sent = email.send_activation()
    return sent