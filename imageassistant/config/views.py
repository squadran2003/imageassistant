from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.middleware import csrf
from django.contrib.sitemaps import Sitemap
from django.core.mail import EmailMessage, get_connection
from django.contrib import messages
from config.forms import ContactForm
import os


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['base', 'users:login', 'users:signup']  # URL names from urls.py

    def location(self, item):
        url = reverse(item)
        url = url.replace("http://", "https://")
        return url


def base(request):
    return render(
        request, 'index.html',{'index_page': True}
    )


def faq(request):
    return render(request, 'faq.html')


def upload_content(request):
    token = csrf.get_token(request)
    # html_content = UploadContent().render(
    #     args=[token],
    # )
    html_content = ""
    return HttpResponse(html_content, content_type='text/html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"ImageAssistant.io - message from {form.cleaned_data['email']}"
            recipient_list = ["cormackandy@hotmail.com"]
            from_email = "no-reply@imageassistant.io"
            message = form.cleaned_data['message']
            with get_connection(
                host=settings.MAILERSEND_SMTP_HOST,
                port=settings.MAILERSEND_SMTP_PORT,
                username=settings.MAILERSEND_SMTP_USERNAME,
                password=settings.MAILERSEND_SMTP_PASSWORD,
                use_tls=True,
                ) as connection:
                    r = EmailMessage(
                          subject=subject,
                          body=message,
                          to=recipient_list,
                          from_email=from_email,
                          connection=connection).send()

            # reset form and add success message
            form = ContactForm()
            form.fields['email'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-black focus:outline-none focus:shadow-outline'
            form.fields['message'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-black focus:outline-none focus:shadow-outline'
            return render(request, 'contact.html#contact-content', {
                'form': form,
                'success': True,
            })
        else:
            if 'message' in form.errors:
                form.fields['message'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-black focus:outline-none focus:shadow-outline required:border-red-500'
            if 'email' in form.errors:
                form.fields['email'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-black focus:outline-none focus:shadow-outline required:border-red-500'
            return render(request, 'contact.html#contact-content', {
                'form': form,
            })

    return render(request, 'contact.html', {
        'form': form,
    })


def stripe_success_return(request):
    return render(request, 'stripe/return.html', {'domain': settings.DOMAIN})


def stripe_checkout(request):
    return render(
        request, 'stripe/checkout.html',
        {'strip_public_key': settings.STRIPE_PUBLISHED_KEY}
    )


def health_check(request):
    try:
        # Check if the database is reachable
        from django.db import connection
        connection.ensure_connection()
        # Check if the cache is reachable
        from django.core.cache import cache
        from celery import shared_task
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)