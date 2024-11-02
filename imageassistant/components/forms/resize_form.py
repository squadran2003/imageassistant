from django_components import Component, register, types

@register("resize_form")
class ResizeForm(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            "width ": kwargs.get("width", ''),
            "height": kwargs.get("height", ''),
            "token": kwargs.get("token", ""),
            "attrs": kwargs.get("attrs", {}),
            "errors": kwargs.get("errors", []),
            "form": kwargs.get("form", None),
        }

    template: types.django_html = """
        {% component_css_dependencies %}
         <div class="row">
            <div class="col s12 m12 lg12">
                <form {% html_attrs attrs %}>
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ token }}">
                    {% for field in form %}
                        <div class="input-field col s12 m12 lg12">
                            {% if not field.errors %}
                                {{ field.label_tag }}
                            {% endif %}
                            {{ field }}
                            {% for error in field.errors %}
                                <span class="helper-text" id="error">{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% endfor %}
                    <a  onclick="htmx.trigger('#image-resize-form', 'submit')" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;"></span>Submit</a>
                </form>
            </div>
        </div>
    """

    css: types.css = """
        .image-resize-form{
            min-width: 100%;
        }
        #error{
            color: red;
        }
    """
