from django_components import Component, register

@register("checkout_test")
class CheckoutTestContent(Component):

    template_name = "test_checkout_template.html"

    def get_context_data(self, service_id, image_id, token, stripe_public_key, **kwargs):
        return {
            "service_id": service_id,
            "image_id": image_id,
            "token": token,
            "stripe_public_key": stripe_public_key,
            "check_out_url": kwargs.get("check_out_url"),
        }

    class Media:
        js = "test_checkout.js"