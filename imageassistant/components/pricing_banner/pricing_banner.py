from django_components import Component, register

@register("pricing_banner")
class PricingBanner(Component):

    template_name = "pricing_banner.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self):
        return {
        }

    class Media:
        css = "pricing_banner.css"
