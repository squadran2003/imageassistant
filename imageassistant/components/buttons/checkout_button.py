from django_components import Component, register, types

@register("checkout_button")
class CheckoutButton(Component):

    template = """
            {% component_css_dependencies %}
            <button type="submit" id="checkout-button" class="waves-effect waves-light btn-large custom-img-checkout-button">{{ label }}</button>
    """
    css = """
        .custom-img-checkout-button {
            background-color: #612785; /* Your custom color */
            margin: 5px 0 0 5px;
            color:white;
        }
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, label):
        return {
            "label": label,
        }