from django_components import Component, register, types

@register("checkout")
class CheckoutContent(Component):

    template: types.django_html = """
        {% load static %}
        <div class="row">
            <div class="col s12  m4 lg4">
                <ul class="collection">
                    <li class="collection-item avatar">
                        <img src="{% static 'img/logo.png' %}" alt="Logo" class="responsive-img">
                        <span class="title">Remove background</span>
                        <p>Quantity: 1<br>
                            Cost: $1.00</p>
                        </p>
                         <form action="/create-checkout-session" method="POST">
                            <input type="hidden" name="csrfmiddlewaretoken" value="{{token}}">
                            <input type="hidden" name="service_id" value="{{service_id}}">
                            <input type="hidden" name="image_id" value="{{image_id}}">
                            {% component "checkout_button" label="Checkout" %} {% endcomponent %}
                        </form>
                    </li>
                </ul>
            </div>
        </div>

    """


    def get_context_data(self, service_id, image_id, token, **kwargs):
        return {
            "service_id": service_id,
            "image_id": image_id,
            "token": token,
        }