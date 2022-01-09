# from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):  # recommended to only pass IDs  & lookup obj as param
    """Task to send an e-mail notification when an order is successfully created."""
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    # used send_mail fn provided by django to send an email notification to the user
    return mail_sent
