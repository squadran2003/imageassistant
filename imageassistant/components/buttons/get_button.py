from django_components import Component, register, types

@register("get_button")
class GetButton(Component):
        # This component takes one parameter, a date string to show in the template
    def get_context_data(self, get_url, label, icon_name, target):
        return {
            "get_url": get_url,
            "label": label,
            "icon_name": icon_name,
            "target": target
        }

    template: types.django_html = """
        {% component_css_dependencies %}
      <a  hx-get={{get_url}} hx-target={{target}}  hx-swap="innerHTML" class="waves-effect btn"><span class="material-icons">{{icon_name}}</span>{{label}}</a>

    """
