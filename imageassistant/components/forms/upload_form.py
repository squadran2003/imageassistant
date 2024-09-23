from django_components import Component, register, types

@register("upload_form")
class UploadForm(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            "attrs": kwargs.get("attrs", {}),
            "error": kwargs.get("errors", None),
        }

    template: types.django_html = """
        {% component_css_dependencies %}
        <form {% html_attrs attrs %}>
            {% csrf_token %}
            <div class="file-field input-field">
                {% component "upload_button" label="Upload image" form_target='#upload-form'  %} {% endcomponent %}
                <div class="file-path-wrapper">
                    <input class="file-path validate file-path-validate-custom" type="text">
                </div>
            </div>
           {% if errors %}
                <div class="col s12 m12 lg12" style="margin-top:5px; color:red">
                    {{errors | safe}}
                </div>
            {% endif %}
        </form>
    """

    css: types.css = """
        .image-resize-form{
            min-width: 100%;
        }
    """
