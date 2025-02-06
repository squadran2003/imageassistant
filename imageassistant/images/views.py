from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from images.models import Image, Service
from images.forms   import ImageUploadForm, ImageResizeForm, CroppingForm, PromptForm as DjangoPromptForm
from images.forms import PromptForm as DjangoPromptForm
from components.buttons.get_button import GetButton
from components.forms.resize_form import ResizeForm
from components.forms.prompt_form import PromptForm
from components.upload_component.upload_component import UploadComponent 
from components.stripe.live_checkout.checkout import CheckoutContent
from components.tools.crop_tool import CropTool
from components.pages.initial_image_page import InitialImagePage
from components.pages.unprocessed_image_page import UnprocessedImagePage
from components.pages.processed_image_page import ProcessedImagePage
from components.pages.main_content import MainContent
from PIL import Image as PILImage
from datetime import datetime
from .tasks import (
    create_greyscale, remove_background,
    resize_image, create_thumbnail, crop_image,
    enhance_image, create_image_from_prompt
)
import stripe
from sentry_sdk import capture_message


stripe.api_key = settings.STRIPE_SECRET_KEY



def add_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.save()
            return redirect("images:get_image", image_id=img.id)
    # if the form is not valid return the main content back
    main_content = MainContent()
    html_content = main_content.render(
        args=[
            form,
            Service.objects.all().order_by('code')
        ]
    )
    return HttpResponse(html_content, content_type='text/html')


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
    enhance_image_service_url = reverse('images:get_prompt_form', args=[6, image_id])
    background_removal_label = 'Remove Background'
    enhance_image_label = 'Enhance Image'
    if not request.user.is_authenticated:
        back_ground_removal_service = Service.objects.get(code=2)
        enhance_image_service = Service.objects.get(code=6)
        if not back_ground_removal_service.free:
            background_removal_service_url = reverse('images:checkout', args=[2, image_id])
            background_removal_label = 'Remove Background: $5'
        if not enhance_image_service.free:
            enhance_image_service_url = reverse('images:checkout', args=[6, image_id])
            enhance_image_label = 'Enhance Image: $3'
    url_context = [
        {
            'url': reverse('images:service', args=[1, image_id]),
            'label': 'Convert to black and white',
            'icon': 'colorize',
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
            'label': 'Create Thumbnail',
            'icon': 'crop_square',
            'target': '#content'
        },
        {
            'url': background_removal_service_url,
            'label': background_removal_label,
            'icon': 'remove',
            'target': '#content'
        },
        {
            'url': reverse('images:crop-tool', args=[5, image_id]),
            'label': 'Crop Image',
            'icon': 'crop',
            'target': '#content'
        },
        {
            'url': enhance_image_service_url,
            'label': enhance_image_label,
            'icon': 'color_lens',
            'target': '#content'
        }
    ]
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
    elif service_id == 6:
        print("Enhancing image")
        if request.method == 'POST':
            form = DjangoPromptForm(request.POST)
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                enhance_image.delay(image_id, prompt)
    elif service_id == 7:
        print("Creating image from prompt")
        print(request.method)
        if request.method == 'POST':
            form = DjangoPromptForm(request.POST)
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                create_image_from_prompt.delay(image_id, prompt)
    poll_url = reverse(
        'images:process_image', args=[
            image_id
        ]
    )
    return render(
        request, 'generate_image.html#img-svg-poll', {'poll_url': poll_url, 'image': img}
    )


def processed_service(request, image_id):
    file = Image.objects.get(pk=image_id)
    # create_image.html#content'
    if not file.processed:
        poll_url = reverse('images:process_image', args=[image_id])
        return render(request, 'generate_image.html#img-svg-poll', {'poll_url': poll_url, 'image': file})
    else:
        print("Image has been processed")
        return render(request, 'generate_image.html#img-processed', {
            'image': file}
        )


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


def get_prompt_form(request, service_id, image_id):
    prompt_form = PromptForm()
    django_prompt_form = DjangoPromptForm()
   
    html_content = prompt_form.render(
        kwargs={
            "attrs": {
                'id': 'prompt-form',
                'hx-post': reverse('images:service', args=[service_id, image_id]),
                'hx-target': "#content",
                'hx-swap': "innerHTML",
            },
            'form': django_prompt_form,
            "errors": []
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
    return_url = f"{settings.DOMAIN}/stripe/return/?session_id={{CHECKOUT_SESSION_ID}}&service_id={service_id}&image_id={image_id}&service_name={service.name}"
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
            return_url=return_url,
            automatic_tax={'enabled': True},
        )
        client_secret = session.client_secret
    except Exception as e:
        # capture message in sentry with info from stripe, like the payment intent id
        capture_message(f"Error creating stripe checkout session: {str(e)}", level='error')
        return HttpResponse(str(e), status=500)
    return JsonResponse(data={'clientSecret':client_secret}, safe=False)


def session_status(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse(data={'status': session.status, 'customer_email': session.customer_details.email}, safe=False)


def generate_image(request):
    form = DjangoPromptForm()
    post_url = reverse('images:generate_image')
    if request.method == 'POST':
        # find out what time the session was started
        if request.session.get('image_assistant_start'):
            start_time = datetime.strptime(request.session['image_assistant_start'], '%Y-%m-%d %H:%M:%S')
            if (datetime.now() - start_time).seconds * 60 * 60 > 24:
                request.session['image_assistant_download_count'] +=1
        if request.session.get('image_assistant_download_count') > 2:
            return render(
                request, 'generate_image.html#content',
                    {
                        'form': form, 'post_url': post_url, 'target': 'this', 'trigger': None,
                        'download_limit_exceeded': True
                    },
                status=400
            )
        form = DjangoPromptForm(request.POST)
        # create a new image object where this response will be stored
        # create a dummy image object
        image = Image.objects.create(image='dummy.png')
        if form.is_valid():
            template = 'generate_image.html#prompt-form'
            redirect_url = reverse('images:service', args=[7, image.id])
            print(redirect_url)
            return render(
                request, template, {
                    'form': form, 'post_url': redirect_url, 
                    'target': '#image-container', 'trigger': 'load'
                },
                status=200
            )
        else:
            print(form.errors)
            template = 'generate_image.html#prompt-form'
            form.fields['prompt'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-50 mb-2 p-2 w-full text-gray-700 focus:outline-none focus:shadow-outline required:border-red-500'
            return render(request, template, {'form': form, 'post_url': post_url, 'target':'this', 'trigger': None}, status=400)
    else:
        template = 'generate_image.html'
        return render(request, template, {'form': form, 'post_url': post_url, 'target':'this', 'trigger': None}, status=200)

