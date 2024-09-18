from django_components import Component, register, types

@register("link")
class Link(Component):

    template: types.django_html = """
     <li><a href="{{ url }}">{{ label }}</a></li>

    """



    def get_context_data(self, url, label):
        return {
            "url": url,
            "label": label
        }
