from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail, send_mass_mail
from accounts.tokens import default_token_generator
from django.conf import settings

from accounts.models import EmailActivation
# @shared_task
# def contact_us(name, email, comments):
#     subject = 'Feedback from {} <{}>'.format(name, email)
#     html_message = render_to_string('feedback/mail_template.html', {'email': email, 'name': name, 'comment': comments})
#     message = 'Message' + '-'*30 + '\n\n{}'.format(comments)
#     sent = send_mail(subject, message, 'ch4rles.co@gmail.com', ['charlesboy49@gmail.com'], html_message=html_message, fail_silently=False)
#     return sent

@shared_task
def EmailVerification(id):
    email = EmailActivation.objects.get(id=id)
    sent = email.send_activation()
    return sent

# from django.utils import timezone
# from datetime import timedelta
# @shared_task
# def SubscriberRemoval():
#     expired = timezone.now() - timedelta(days=3)
#     subscribers = Subscriber.objects.filter(active=False, timestamp__lte=expired)
#     if subscribers:
#         temp = [x.email for x in subscribers]
#         for subscriber in subscribers:
#             subscriber.delete()
#         return "{} has been removed successfully".format(temp)
#     return "0 email deleted"

# @shared_task
# def Daily_Post_Notification():
#     daily = timezone.now() - timedelta(days=1)
#     posts = Post.objects.filter(publish_date__gte=daily)
#     if posts:
#         subscribers = Subscriber.objects.filter(active=True)
#         emails = [x.email for x in subscribers]
#         subject = "Incase you missed it"
#         message = 'Message' + '-'*30 + '\n\n{}'.format(subject)
#         html = render_to_string("subscription/post_notification.html", {
#             'posts': posts,
#             'domain': "http://192.168.43.195:8000",})
#         send_mail(subject, message, settings.EMAIL_HOST_USER, emails, html_message=html, fail_silently=False)
#         return True
#     return False
# @shared_task
# def test():
#     return "Hello !!!"