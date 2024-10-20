from django_components import Component, register

@register("banner")
class Banner(Component):

    template_name = "banner.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self):
        return {
        }

    class Media:
        css = "banner.css"
