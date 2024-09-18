from django_components import Component, register, types

@register("get_button")
class GetButton(Component):
        # This component takes one parameter, a date string to show in the template
    def get_context_data(self, get_url, label, icon_name):
        return {
            "get_url": get_url,
            "label": label,
            "icon_name": icon_name
        }

    template: types.django_html = """
        {% component_css_dependencies %}
      <a  hx-get={{get_url}} hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;">{{icon_name}}</span>{{label}}</a>

    """

    css: types.css = """
         .custom-img-transform-button{
            background-color: #284db7; /* Your custom color */
            margin: 5px 0 0 5px;
            color:white;

        }
        .custom-img-transform-button:hover {
            background-color:  #6d83c3; /* Your custom color */
        }
    """
