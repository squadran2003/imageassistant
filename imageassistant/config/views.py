from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.conf import settings
from django.middleware import csrf
from components.pages.upload import UploadContent
import os


def base(request):
    return render(request, 'index.html')


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
    if settings.DEBUG:
        return render(request, 'stripe/checkout_test.html')
    return render(request, 'stripe/checkout.html')