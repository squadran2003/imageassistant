from django_components import Component, register, types
from django.urls import reverse

@register("upload_component")
class UploadComponent(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            'form': kwargs.get('form', ''),
            'attrs': {
                'id': kwargs.get('id', ''),
                'hx-target': kwargs.get('target', ''),
                'hx-swap': kwargs.get('swap', ''),
                'hx-post': reverse(kwargs.get('url', '')),
                'method': 'post',
                'enctype': 'multipart/form-data',
            }
        }

    template_name = "./upload_component.html"

    class Meta:
        css = "./upload_component.css"
