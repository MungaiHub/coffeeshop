# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order

@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, **kwargs):
    if instance.status == 'completed':
        subject = f"Order #{instance.id} Completed"
        message = f"Dear {instance.customer_name},\n\nYour order has been completed. Thank you for shopping with us!"
        from_email = "noreply@coffeeshop.com"  # Replace with your email
        recipient_list = [instance.customer_email]
        send_mail(subject, message, from_email, recipient_list)