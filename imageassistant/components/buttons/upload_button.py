from django_components import Component, register, types

@register("UploadButton")
class UploadButton(Component):

    template: types.django_html = """
        <div class="btn custom-img-upload-button pulse">
            <span>{{label}}</span>
            <input type="file" name="image" hx-indicator="#indicator" onchange="htmx.trigger('{{form_target}}', 'submit')">
        </div>

    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, form_target, label):
        return {
            "form_target": form_target,
            "label": label,
        }