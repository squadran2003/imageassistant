from django_components import Component, register, types
from django.urls import reverse

@register("upload_form")
class UploadForm(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            "attrs": {
                "id": kwargs.get("id", ""),
                "hx-target": kwargs.get("target", ""),
                "hx-swap": kwargs.get("swap", ""),
                "hx-post": reverse(kwargs.get("url", "")),
                "method": "post",
                "enctype": "multipart/form-data",
                "hx-indicator": "#indicator"
            }
        }

    template_name = "./upload_form_template.html"

    class Meta:
        css = "upload_form.css"
        js = "upload_form.js"
