from django_components import Component, register, types

@register("upload")
class UploadContent(Component):

    template = """
            <div class="row">
                <div class="col s12 m12 lg12 x12 custom-margin-top">
                    <div id="service-buttons">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col s12 custom-margin-top">
                    <div id="upload-form-container">
                        {% component "upload_form"  token="{{ csrf_token }}" attrs:id="upload-form" attrs:hx-post="{% url 'images:add' %}" attrs:hx-target="#img-container" attrs:hx-swap="innerHTML"  attrs:enctype="multipart/form-data" %} {% endcomponent %}
                    </div>
                    <div class="indeterminate file-path-validate-custom" style="width: 100%"></div>
                    </div>
                    <div class="progress htmx-indicator" id="indicator">
                        <div class="indeterminate"></div>
                    </div>
                    <div id="img-container" class="img-container">
                    </div>
            </div>
        </div>
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, csrf_token, **kwargs):
        return {
            "csrf_token": csrf_token,
   
        }