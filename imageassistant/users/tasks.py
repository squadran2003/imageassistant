from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from users.models import CustomUser
import datetime
import sentry_sdk




@shared_task
def send_email_task(user_id, amount, credits_received,payment_intent_id=None, payment_intent_created=None):
    """
    A Celery task to send an email.
    """

    try:
        user = CustomUser.objects.get(id=user_id)
        name = user.first_name or user.email
        transaction_date = datetime.datetime.now()  # Default to now
        if payment_intent_created:
            try:
                # Convert string to int if needed
                if isinstance(payment_intent_created, str):
                    payment_intent_created = int(payment_intent_created)
                transaction_date = datetime.datetime.fromtimestamp(payment_intent_created)
            except (ValueError, TypeError):
                # If conversion fails, use current time
                transaction_date = datetime.datetime.now()
        # Prepare email context
        context = {
            'user': name,
            'amount': amount,
            'credits_received': credits_received,
            'transaction_id': payment_intent_id,
            'transaction_date': transaction_date,
            'company_name': 'ImageAssistant.io',
            'support_email': 'cormackandy@hotmail.com',
        }
        
        # Render email templates
        html_message = render_to_string('users/emails/receipt.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=f'Receipt for your ImageAssistant.io credit purchase - ${amount}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Email sent to {user.email} for amount ${amount} with credits received: {credits_received}")
        sentry_sdk.capture_message('Email sent successfully', {
            'user_email': user.email,
            'amount': amount,
            'credits_received': credits_received,
            'transaction_id': payment_intent_id,
        })
        
    except Exception as e:
        print(f"Failed to send email to {user.email}: {e}")
        sentry_sdk.capture_exception(e, {
            'user_email': user.email,
            'amount': amount,
            'credits_received': credits_received,
            'transaction_id': payment_intent_id,
        })

