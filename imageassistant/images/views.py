from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from images.models import Image, Service
from images.forms   import ImageUploadForm, ImageResizeForm, CroppingForm
from components.buttons.get_button import GetButton
from components.forms.resize_form import ResizeForm
from components.upload_component.upload_component import UploadComponent 
from components.stripe.live_checkout.checkout import CheckoutContent
from components.tools.crop_tool import CropTool
from components.pages.initial_image_page import InitialImagePage
from components.pages.unprocessed_image_page import UnprocessedImagePage
from components.pages.processed_image_page import ProcessedImagePage
from components.pages.main_content import MainContent
from PIL import Image as PILImage
from .tasks import (
    create_greyscale, remove_background,
    resize_image, create_thumbnail, crop_image
)
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def add_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.save()
            return redirect("images:get_image", image_id=img.id)
        else:
            main_content = MainContent()
            html_content = main_content.render(
                args=[form]
            )
            return HttpResponse(html_content, content_type='text/html')
    return HttpResponse("", content_type='text/html')


def get_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    page = InitialImagePage()
    html_content = page.render(
        kwargs={
            # url to get the service buttons
            "hx_get_url": reverse('images:get_service_buttons', args=[image_id]),
            "hx_target": "#service-buttons",
            "hx_swap": "innerHTML",
            "hx_trigger": "load",
            "image_url": image.image.url
        }
    )
    return HttpResponse(html_content, content_type='text/html')


def get_service_buttons(request, image_id):
    # for a removebackground service. If logged in then function as normal
    # else present with a stripe form
    # when stripe says payemnt is successful, then process background removal
    background_removal_service_url = reverse('images:service', args=[2, image_id])
    if not request.user.is_authenticated:
        background_removal_service_url = reverse('images:checkout', args=[2, image_id])
    url_context = [
        {
            'url': reverse('images:service', args=[1, image_id]),
            'label': 'Convert to black and white',
            'icon': 'colorize',
            'target': '#content'
        },
        {
            'url': background_removal_service_url,
            'label': 'Remove background',
            'icon': 'lock',
            'target': '#content'
        },
        {
            'url': reverse('images:resize-form', args=[image_id]),
            'label': 'Resize',
            'icon': 'transform',
            'target': '#content'
        },
        {
            'url': reverse('images:service', args=[4, image_id]),
            'label': 'Create thumbnail',
            'icon': 'image',
            'target': '#content'
        },
        {
            'url': reverse('images:crop-tool', args=[5, image_id]),
            'label': 'Crop Image',
            'icon': 'crop',
            'target': '#content'
        }
    ]
    # if not settings.DEBUG:
    #     url_context = [
    #         {
    #             'url': reverse('images:service', args=[1, image_id]),
    #             'label': 'Convert to black and white',
    #             'icon': 'colorize',
    #             'target': '#content'
    #         },
    #         {
    #             'url': reverse('images:resize-form', args=[image_id]),
    #             'label': 'Resize',
    #             'icon': 'transform',
    #             'target': '#content'
    #         },
    #         {
    #             'url': reverse('images:service', args=[4, image_id]),
    #             'label': 'Create thumbnail',
    #             'icon': 'image',
    #             'target': '#content'
    #         },
    #         {
    #             'url': reverse('images:crop-tool', args=[5, image_id]),
    #             'label': 'Crop Image',
    #             'icon': 'crop',
    #             'target': '#content'
    #         }
    #     ]
    html_content = ''
    for context in url_context:
        button = GetButton()
        html_content += button.render(
            args=[context['url'], context['label'], context['icon'], context['target']]
        )
    return HttpResponse(html_content, content_type='text/html')


def service(request, service_id, image_id):
    img = Image.objects.get(pk=image_id)
    img.processed = False
    img.save()
    if service_id == 1:
        print("Creating greyscale image")
        create_greyscale.delay(image_id)
    elif service_id == 2:
        print("Removing background")
        remove_background.delay(image_id)
    elif service_id == 4:
        print("Creating thumbnail")
        create_thumbnail.delay(image_id)
    elif service_id == 5:
        print("Cropping image")
        if request.method == 'POST':
            token = csrf.get_token(request)
            form = CroppingForm(request.POST)
            if form.is_valid():
                crop_image.delay(
                    image_id, form.cleaned_data['x'], form.cleaned_data['y'],
                    form.cleaned_data['width'], form.cleaned_data['height']
                )
            else:
                crop_tool = CropTool()
                html_content = crop_tool.render(
                    args=[img.image.url, form, service_id, image_id, token]
                )
                return HttpResponse(html_content, content_type='text/html')
        # crop_image.delay(image_id, x , y, width, height)
    unprocessed_page = UnprocessedImagePage()
    html_content = unprocessed_page.render(
        kwargs={
            "hx_get_url": reverse('images:process_image', args=[image_id]),
            "hx_target": "#content",
            "hx_swap": "innerHTML",
            "hx_trigger": "load delay:3s",
            "image_url": img.image.url
        }
    )
    return HttpResponse(html_content, content_type='text/html')


def processed_service(request, image_id):
    file = Image.objects.get(pk=image_id)
    if not file.processed:
        unprocessed_image_page = UnprocessedImagePage()
        html_content = unprocessed_image_page.render(
            kwargs={
                "hx_get_url": reverse('images:process_image', args=[image_id]),
                "hx_target": "#content",
                "hx_swap": "innerHTML",
                "hx_trigger": "load delay:3s",
                "image_url": file.image.url
            }
        )
        return HttpResponse(html_content, content_type='text/html', status=200)
    else:
        processed_image_page = ProcessedImagePage()
        html_content = processed_image_page.render(
            args=[file]
        )
        return HttpResponse(html_content, content_type='text/html', status=286)


def resize_form_html(request, image_id):
    """send a form to the client to get the width and height of the image"""
    form = ImageResizeForm()
    # this is the url that the form will post to
    post_url = reverse('images:resize-form', args=[image_id])
    # this is the component that will be rendered
    resize_form = ResizeForm()
    data = {
            'id': 'image-resize-form',
            'hx-post': post_url,
            'hx-target': "#content",
            'hx-swap': "innerHTML",
    }
    if request.method == 'POST':
        form = ImageResizeForm(request.POST)
        if form.is_valid():
            width = int(request.POST['width'])
            height = int(request.POST['height'])
            resize_image.delay(
                image_id, width, height
            )
            unprocessed_image_page = UnprocessedImagePage()
            html_content = unprocessed_image_page.render(
                kwargs={
                    "hx_get_url": reverse(
                        'images:process_image', args=[image_id]
                    ),
                    "hx_target": "#content",
                    "hx_swap": "innerHTML",
                    "hx_trigger": "load delay:3s",
                    "image_url": ""
                }
            )
            return HttpResponse(html_content, content_type='text/html')
    html_content = resize_form.render(
        kwargs={
            "attrs": data,
            "form": form
        }

    )
    return HttpResponse(html_content, content_type='text/html')


def crop_tool_content(request, service_id, image_id):
    image = Image.objects.get(pk=image_id)
    form = CroppingForm()
    form.service_id = service_id
    form.image_id = image_id
    crop_tool = CropTool()
    html_content = crop_tool.render(
        args=[image.image.url, form, service_id, image_id]
    )
    return HttpResponse(html_content, content_type='text/html')


def get_upload_form(request):
    form = UploadComponent()
    post_url = reverse('images:add')
    token = csrf.get_token(request)
    attrs = {
        'id': 'upload-form',
        'hx-post': post_url,
        'hx-target': "#img-container",
        "hx-swap": "innerHTML",
        "enctype": "multipart/form-data"
    }
    html_content = form.render(
        args=[token],
        kwargs={
            "attrs": attrs,
            "errors": []
        }
    )
    return HttpResponse(html_content, content_type='text/html')


def get_checkout_content(request, service_id, image_id):
    token = csrf.get_token(request)
    check_out_url = reverse('images:create_checkout_session', args=[service_id, image_id])
    html_content = ''
    checkout_content = CheckoutContent()
    html_content = checkout_content.render(
        args=[service_id, image_id, token, settings.STRIPE_PUBLIC_KEY],
        kwargs={
            "check_out_url": check_out_url,
        }
    )
    return HttpResponse(html_content, content_type='text/html')


def create_checkout_session(request, service_id, image_id):
    service = Service.objects.get(code=service_id)
    client_secret = ''
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
    # if no price id is set, then redirect to the service page as the service doesnt require payment
    if not service.stripe_price_id:
        return redirect('images:service', service_id, image_id)
    try:
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': service.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=f"{settings.DOMAIN}/stripe/return/?session_id={{CHECKOUT_SESSION_ID}}&service_id={service_id}&image_id={image_id}",
            automatic_tax={'enabled': True},
        )
        client_secret = session.client_secret
    except Exception as e:
        return HttpResponse(str(e), status=500)
    return JsonResponse(data={'clientSecret':client_secret}, safe=False)


def session_status(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse(data={'status': session.status, 'customer_email': session.customer_details.email}, safe=False)

