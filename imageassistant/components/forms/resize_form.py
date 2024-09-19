from django_components import Component, register, types

@register("resize_form")
class ResizeForm(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, post_url, token, width='', height='', errors=[]):
        return {
            "post_url": post_url,
            "token": token,
            "errors": errors,
            "width": width,
            "height": height
        }

    template: types.django_html = """
        {% component_css_dependencies %}
            <form id="image-resize-form" hx-post={{ post_url }} hx-target="#img-container"  hx-swap="innerHTML">
                <input type="hidden" name="csrfmiddlewaretoken" value={{token}}>
                <div class="col s12 m12 lg12">
                    <input id="width" name="width" type="number" class="validate" value={{width}}>
                    <label for="width">Width in pixels</label>
                </div>
                <div class="col s12 m12 lg12">
                    <input id="height" name="height" type="number" class="validate" value={{height}}>
                    <label for="height">Height in pixels</label>
                </div>
                 <div class="col s12 m12 lg12" style="margin-top:5px;">
                    <a  onclick="htmx.trigger('#image-resize-form', 'submit')" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;"></span>Submit</a>
                </div>
                {% if errors %}
                     content = "<ul>"
                    {% for k, v in errors %}
                        errors += f"<li style='color:red'>{k}: {v}</li>"
                        errors += "</ul>"
                    {% endfor %}
                {% endif %}
            </form>

    """

    css: types.css = """
        .image-resize-form{
            min-width: 100%;
        }
    """
