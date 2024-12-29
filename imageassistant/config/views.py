from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.middleware import csrf
from images.forms import ImageUploadForm
from images.models import Service
import os


def base(request):
    form = ImageUploadForm()
    services = Service.objects.all().order_by('code')
    return render(
        request, 'index.html',
        {'form': form, 'MEDIA_URL': settings.MEDIA_URL, 'services': services}
    )


def upload_content(request):
    token = csrf.get_token(request)
    # html_content = UploadContent().render(
    #     args=[token],
    # )
    html_content = ""
    return HttpResponse(html_content, content_type='text/html')


def about(request):
    html_content = """
        <div class="row">
            <div class="col s12 m12">
                <h5>About content</h5>
                <p>This is the left column content.</p>
            </div>
        </div>
    """
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