from django_components import Component, register


@register("crop_tool")
class CropTool(Component):

    template_name = "crop_tool.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, img_url, form, service_id, image_id, token):
        return {
            "img_url": img_url,
            "form": form,
            "service_id": service_id,
            "image_id": image_id,
            "token": token
        }
