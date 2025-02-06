from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.middleware import csrf
from django.contrib.sitemaps import Sitemap
from images.forms import ImageUploadForm
from images.models import Service
import os
from datetime import datetime


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['base', 'images:generate_image']  # URL names from urls.py

    def location(self, item):
        return reverse(item)


def base(request):
    form = ImageUploadForm()
    services = Service.objects.all().order_by('code')
    if request.session.get('image_assistant_start'):
        start_time = datetime.strptime(request.session['image_assistant_start'], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - start_time).seconds * 60 *60 > 24:
            request.session['image_assistant_start'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session['image_assistant_download_count'] = 0
    else:
        request.session['image_assistant_start'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['image_assistant_download_count'] = 0
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
    html_content = """
        <div class="row">
            <div class="col s12 m12">
                <h5>Contact content</h5>
                <p>This is the left column content.</p>
            </div>
        </div>
    """
    return HttpResponse(html_content, content_type='text/html')


def stripe_success_return(request):
    return render(request, 'stripe/return.html', {'domain': settings.DOMAIN})


def stripe_checkout(request):
    return render(
        request, 'stripe/checkout.html',
        {'strip_public_key': settings.STRIPE_PUBLISHED_KEY}
    )