from django_components import Component, register, types

@register("initial_image_page")
class InitialImagePage(Component):

    template = """
           <div class="row">
                <div class="col s12 m12 l12 xl12 custom-margin-top">
                    <div id="service-buttons">
                    </div>
                </div>
                <div class="col s12 m12 l12 xl12 custom-margin-top">
                    <img {% html_attrs attrs default="" %}>
                </div>
         </div>
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            "attrs": {
                "hx-get": kwargs.get("hx_get_url"),
                "hx-target": kwargs.get("hx_target"),
                "hx-swap": kwargs.get("hx_swap"),
                "hx-trigger": kwargs.get("hx_trigger"),
                "src": kwargs.get("image_url"),
                "alt": "Processed Image",
                "class": "responsive-img"
            }

        }
