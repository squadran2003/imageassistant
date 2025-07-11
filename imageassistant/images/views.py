from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django import forms
from images.models import Image, Service
from images.forms   import ImageUploadForm, ImageResizeForm, CroppingForm, PromptForm as DjangoPromptForm
from images.forms import PromptForm as DjangoPromptForm
from users.models import FeatureFlag, Credit
from datetime import datetime
from .tasks import (
    create_greyscale, remove_background,
    create_thumbnail, create_image_outline_task,
    enhance_image, create_image_from_prompt
)
import stripe
from sentry_sdk import capture_message
from django.db.models import Q


stripe.api_key = settings.STRIPE_SECRET_KEY



# def add_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             img = form.save(commit=False)
#             img.save()
#             return redirect("images:get_image", image_id=img.id)
#     # if the form is not valid return the main content back
#     main_content = MainContent()
#     html_content = main_content.render(
#         args=[
#             form,
#             Service.objects.all().order_by('code')
#         ]
#     )
#     return HttpResponse(html_content, content_type='text/html')


# def get_image(request, image_id):
#     image = Image.objects.get(pk=image_id)
#     page = InitialImagePage()
#     html_content = page.render(
#         kwargs={
#             # url to get the service buttons
#             "hx_get_url": reverse('images:get_service_buttons', args=[image_id]),
#             "hx_target": "#service-buttons",
#             "hx_swap": "innerHTML",
#             "hx_trigger": "load",
#             "image_url": image.image.url
#         }
#     )
#     return HttpResponse(html_content, content_type='text/html')


# def get_service_buttons(request, image_id):
#     # for a removebackground service. If logged in then function as normal
#     # else present with a stripe form
#     # when stripe says payemnt is successful, then process background removal
#     background_removal_service_url = reverse('images:service', args=[2, image_id])
#     enhance_image_service_url = reverse('images:get_prompt_form', args=[6, image_id])
#     background_removal_label = 'Remove Background'
#     enhance_image_label = 'Enhance Image'
#     if not request.user.is_authenticated:
#         back_ground_removal_service = Service.objects.get(code=2)
#         enhance_image_service = Service.objects.get(code=6)
#         if not back_ground_removal_service.free:
#             background_removal_service_url = reverse('images:checkout', args=[2, image_id])
#             background_removal_label = 'Remove Background: $5'
#         if not enhance_image_service.free:
#             enhance_image_service_url = reverse('images:checkout', args=[6, image_id])
#             enhance_image_label = 'Enhance Image: $3'
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
#             'label': 'Create Thumbnail',
#             'icon': 'crop_square',
#             'target': '#content'
#         },
#         {
#             'url': background_removal_service_url,
#             'label': background_removal_label,
#             'icon': 'remove',
#             'target': '#content'
#         },
#         {
#             'url': reverse('images:crop-tool', args=[5, image_id]),
#             'label': 'Crop Image',
#             'icon': 'crop',
#             'target': '#content'
#         },
#         {
#             'url': enhance_image_service_url,
#             'label': enhance_image_label,
#             'icon': 'color_lens',
#             'target': '#content'
#         }
#     ]
#     html_content = ''
#     for context in url_context:
#         button = GetButton()
#         html_content += button.render(
#             args=[context['url'], context['label'], context['icon'], context['target']]
#         )
#     return HttpResponse(html_content, content_type='text/html')


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
    # elif service_id == 5:
    #     print("Cropping image")
    #     if request.method == 'POST':
    #         token = csrf.get_token(request)
    #         form = CroppingForm(request.POST)
    #         if form.is_valid():
    #             crop_image.delay(
    #                 image_id, form.cleaned_data['x'], form.cleaned_data['y'],
    #                 form.cleaned_data['width'], form.cleaned_data['height']
    #             )
    #         else:
    #             crop_tool = CropTool()
    #             html_content = crop_tool.render(
    #                 args=[img.image.url, form, service_id, image_id, token]
    #             )
    #             return HttpResponse(html_content, content_type='text/html')
    elif service_id == 6:
        print("Enhancing image")
        if request.method == 'POST':
            form = DjangoPromptForm(request.POST)
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                enhance_image.delay(image_id, prompt)
    elif service_id == 7:
        print("Creating image from prompt")
        if request.method == 'POST':
            form = DjangoPromptForm(request.POST)
            if form.is_valid():
                prompt = form.cleaned_data['prompt']
                create_image_from_prompt.delay(image_id, prompt)
    poll_url = reverse(
        'images:process_service', args=[
            service_id,
            image_id
        ]
    )
    return render(
        request, 'images/generate_image.html#img-svg-poll', {'poll_url': poll_url, 'image': img}
    )


def process_service(request, service_id, image_id):
    file = Image.objects.get(pk=image_id)
    service = Service.objects.get(code=service_id)
    file.save()
    # create_image.html#content'
    if file.processed:
        template_name = ''
        match service_id:
            case 7:
                template_name = 'images/generate_image.html#img-processed'
            case 2:
                template_name = 'images/remove_background.html#processed-image'
            case 8:
                template_name = 'images/create_image_outline.html#processed-image'
        return render(request, template_name, {
                'image': file,
                'service_id': service_id,
                'cost': service.tokens,
                'free': True,
                'payment_made': None
            }, status=286
        )
    else:
        template_name = ''
        match service_id:
            case 7:
                template_name = 'images/generate_image.html#partial-spinner'
            case 2:
                template_name = 'images/remove_background.html#processing-image'
            case 8:
                template_name = 'images/create_image_outline.html#processing-image'
        poll_url = reverse('images:process_service', args=[service_id, image_id])
        return TemplateResponse(request, template_name, {
            'poll_url': poll_url,
            'trigger': 'load delay:3s',
            'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-10 text-center'
        })


# def resize_form_html(request, image_id):
#     """send a form to the client to get the width and height of the image"""
#     form = ImageResizeForm()
#     # this is the url that the form will post to
#     post_url = reverse('images:resize-form', args=[image_id])
#     # this is the component that will be rendered
#     resize_form = ResizeForm()
#     data = {
#             'id': 'image-resize-form',
#             'hx-post': post_url,
#             'hx-target': "#content",
#             'hx-swap': "innerHTML",
#     }
#     if request.method == 'POST':
#         form = ImageResizeForm(request.POST)
#         if form.is_valid():
#             width = int(request.POST['width'])
#             height = int(request.POST['height'])
#             resize_image.delay(
#                 image_id, width, height
#             )
#             unprocessed_image_page = UnprocessedImagePage()
#             html_content = unprocessed_image_page.render(
#                 kwargs={
#                     "hx_get_url": reverse(
#                         'images:process_image', args=[image_id]
#                     ),
#                     "hx_target": "#content",
#                     "hx_swap": "innerHTML",
#                     "hx_trigger": "load delay:3s",
#                     "image_url": ""
#                 }
#             )
#             return HttpResponse(html_content, content_type='text/html')
#     html_content = resize_form.render(
#         kwargs={
#             "attrs": data,
#             "form": form
#         }

#     )
#     return HttpResponse(html_content, content_type='text/html')


# def crop_tool_content(request, service_id, image_id):
#     image = Image.objects.get(pk=image_id)
#     form = CroppingForm()
#     form.service_id = service_id
#     form.image_id = image_id
#     crop_tool = CropTool()
#     html_content = crop_tool.render(
#         args=[image.image.url, form, service_id, image_id]
#     )
#     return HttpResponse(html_content, content_type='text/html')


# def get_upload_form(request):
#     form = UploadComponent()
#     post_url = reverse('images:add')
#     token = csrf.get_token(request)
#     attrs = {
#         'id': 'upload-form',
#         'hx-post': post_url,
#         'hx-target': "#img-container",
#         "hx-swap": "innerHTML",
#         "enctype": "multipart/form-data"
#     }
#     html_content = form.render(
#         args=[token],
#         kwargs={
#             "attrs": attrs,
#             "errors": []
#         }
#     )
#     return HttpResponse(html_content, content_type='text/html')


def build_checkout_session(request, service_id, image_id):
    return render(
        request, "images/generate_image.html#stripe-checkout-form",
        {
            'service_id': service_id, 'image_id': image_id,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY
        },
        status=200
    )


# def get_prompt_form(request, service_id, image_id):
#     prompt_form = PromptForm()
#     django_prompt_form = DjangoPromptForm()

#     html_content = prompt_form.render(
#         kwargs={
#             "attrs": {
#                 'id': 'prompt-form',
#                 'hx-post': reverse('images:service', args=[service_id, image_id]),
#                 'hx-target': "#content",
#                 'hx-swap': "innerHTML",
#             },
#             'form': django_prompt_form,
#             "errors": []
#         }
#     )
#     return HttpResponse(html_content, content_type='text/html')


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
        print("Error creating stripe checkout session")
        return HttpResponse(str(e), status=500)
    return JsonResponse(data={'clientSecret':client_secret}, safe=False)


def session_status(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse(data={'status': session.status, 'customer_email': session.customer_details.email}, safe=False)

@login_required(login_url='custom_users:login')
def generate_image(request):
    form = DjangoPromptForm()
    post_url = reverse('images:generate_image')
    if request.method == 'POST':
        form = DjangoPromptForm(request.POST)
        # create a new image object where this response will be stored
        # create a dummy image object
        image, _ = Image.objects.get_or_create(
            image='dummy.png', user=request.user,
            defaults={
                'created': datetime.now(),
                'processed': False,
            }

        )
        if form.is_valid():
            if request.user.featureflag_set.filter(name='show_credits').exists() and request.user.credit.total < 1:
                # if the user has no credits, then redirect to the stripe checkout page
                template = 'images/generate_image.html#content'
                form.fields['prompt'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-[#1e1a1a] focus:outline-none focus:shadow-outline required:border-red-500'
                form.add_error("prompt", "You have no credits left. Please purchase more credits to generate images.")
                return render(request, template, {
                    'form': form, 'post_url': post_url,
                    'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
                }, status=400)
            template = 'images/generate_image.html#content'
            # add in the aspect ratio the user has selected
            image.aspect_ratio = form.cleaned_data['aspect_ratio']
            image.prompt = form.cleaned_data['prompt']
            image.save()
            prompt = form.cleaned_data['prompt']
            create_image_from_prompt.delay(image.id, prompt)
            poll_url = reverse('images:process_service', args=[7, image.id])
            return TemplateResponse(request, template, {
                'poll_url': poll_url,
                'form': form,
                'trigger': 'every 3s',
                'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 text-center'
            })
        else:
            template = 'images/generate_image.html#content'
            form.fields['prompt'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-[#1e1a1a] focus:outline-none focus:shadow-outline required:border-red-500'
            return render(request, template, {
                'form': form, 'post_url': post_url,
                'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
            }, status=400)
    else:
        template = 'images/generate_image.html'
        return TemplateResponse(request, template, {
            'form': form,
            'post_url': post_url,
            'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
        }, status=200)


@login_required(login_url='custom_users:login')
def dashboard(request):
    return render(request, 'images/dashboard.html', {'images': Image.objects.filter(user=request.user).order_by('-created')})


def search(request):
    query = request.GET.get('q')
    search_terms = query.split(" ")
    q_objects = [Q(prompt__icontains=term) for term in search_terms]

    # Combine with OR logic
    combined_q = Q()
    for q in q_objects:
        combined_q |= q

    images = Image.objects.filter(combined_q)
    if not images:
        return render(request, 'index.html#images', {
            'no_search_images': True,
            'queried': True, 'query': query
        })
    return render(request, 'index.html#searched-images', {
            'images': images, 'no_search_images': True,
            'queried': True, 'query': query
        }
    )

@login_required(login_url='custom_users:login')
def remove_image_background(request):
    error = False
    form = ImageUploadForm()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.featureflag_set.filter(name='show_credits').exists() and request.user.credit.total < 1:
                # if the user has no credits, then redirect to the stripe checkout page
                template = 'images/generate_image.html#content'
                form.fields['prompt'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-[#1e1a1a] focus:outline-none focus:shadow-outline required:border-red-500'
                form.add_error("prompt", "You have no credits left. Please purchase more credits to generate images.")
                return render(request, template, {
                    'form': form, 'post_url': reverse('images:remove_image_background'),
                    'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
                }, status=400)
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            # process the image
            remove_background.delay(form.id)
            poll_url = reverse('images:process_service', args=[2,form.id])
            template = 'images/remove_background.html#processing-image'
            return TemplateResponse(request, template, {
                'poll_url': poll_url,
                'form': form,
                'trigger': 'every 3s',
            })
        else:
            return render(request, 'images/remove_background.html#upload-form', {
                'form': form, 'error': error,
                'post_url': reverse('images:remove_image_background'),
                'target': '#content',
                'trigger': ''
            }, status=400)
    else:
        template = 'images/remove_background.html'
        return TemplateResponse(request, template, {
            'form': form,
            'target': '#content',
            'trigger': '',
            'post_url': reverse('images:remove_image_background'),
            'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
        }, status=200)


@login_required(login_url='custom_users:login')
def create_image_outline(request):
    error = False
    form = ImageUploadForm()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.featureflag_set.filter(name='show_credits').exists() and request.user.credit.total < 1:
                # if the user has no credits, then redirect to the stripe checkout page
                template = 'images/generate_image.html#content'
                form.fields['prompt'].widget.attrs['class'] = 'shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-[#1e1a1a] focus:outline-none focus:shadow-outline required:border-red-500'
                form.add_error("prompt", "You have no credits left. Please purchase more credits to generate images.")
                return render(request, template, {
                    'form': form, 'post_url': reverse('images:remove_image_background'),
                    'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
                }, status=400)
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            # process the image
            print(create_image_outline)
            create_image_outline_task.delay(form.id)
            poll_url = reverse('images:process_service', args=[8,form.id])
            template = 'images/create_image_outline.html#processing-image'
            return TemplateResponse(request, template, {
                'poll_url': poll_url,
                'form': form,
                'trigger': 'every 3s',
            })
        else:
            return render(request, 'images/create_image_outline.html#upload-form', {
                'form': form, 'error': error,
                'post_url': reverse('images:remove_image_background'),
                'target': '#content',
                'trigger': ''
            }, status=400)
    else:
        template = 'images/create_image_outline.html'
        return TemplateResponse(request, template, {
            'form': form,
            'target': '#content',
            'trigger': '',
            'post_url': reverse('images:create_image_outline'),
            'spinner_class': 'animate-spin h-16 w-16 text-indigo-600 mt-4 htmx-indicator'
        }, status=200)
    
def pricing(request):
    return render(request, 'images/prices.html', {
        'services': Service.objects.all().order_by('code'),
    })