from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.middleware import csrf
from django.contrib.sitemaps import Sitemap
from django.core.mail import EmailMessage, get_connection
from django.contrib import messages
from config.forms import ContactForm
from images.forms import ImageUploadForm
from images.models import Service
import os


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['base', 'images:generate_image']  # URL names from urls.py

    def location(self, item):
        url = reverse(item)
        url = url.replace("http://", "https://")
        return url


def base(request):
    form = ImageUploadForm()
    services = Service.objects.all().order_by('code')
    return render(
        request, 'index.html',
        {'form': form, 'services': services}
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
            messages.success(request, 'Message sent!')
            form.fields['email'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-white focus:outline-none focus:shadow-outline'
            form.fields['message'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-white focus:outline-none focus:shadow-outline'
            return render(request, 'contact.html#content', {
                'form': form,
            })
        else:
            messages.error(request, 'There was an error with your message.')
            if 'message' in form.errors:
                form.fields['message'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-white focus:outline-none focus:shadow-outline required:border-red-500'
            if 'email' in form.errors:
                form.fields['email'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-white focus:outline-none focus:shadow-outline required:border-red-500'
            return render(request, 'contact.html#content', {
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