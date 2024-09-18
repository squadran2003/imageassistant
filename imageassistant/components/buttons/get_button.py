from django_components import Component, register, types

@register("GetButton")
class GetButton(Component):

    template: types.django_html = """
      <a  hx-get={{get_url}} hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:black;">{{icon_name}}</span>{{label}}</a>

    """

    css: types.css = """
        .custom-img-transform-button{
            background-color: #ffffff; /* Your custom color */
            margin: 5px,0,0,5px;
            color:black;
            min-width: 100%;
            margin-top: 5px;

        }
        .custom-img-transform-button:hover {
            background-color: lightgray;
        }
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, get_url, label, icon_name):
        return {
            "get_url": get_url,
            "label": label,
            "icon_name": icon_name
        }
