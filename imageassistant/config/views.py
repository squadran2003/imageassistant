from django.shortcuts import render
from django.http import HttpResponse  # Import HttpResponse class
import os


def index(request):
    return render(request, 'index.html')


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