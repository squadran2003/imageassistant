from django_components import Component, register, types

@register("upload_button")
class UploadButton(Component):

    template = """
        <div class="btn custom-img-upload-button pulse">
            <span>{{label}}</span>
            <input type="file" name="image" hx-indicator="#indicator" onchange="htmx.trigger('{{form_target}}', 'submit')">
        </div>

    """
    css = """
       .custom-img-upload-button{
            background-color: #284db7; /* Your custom color */
            margin: 5px 0 0 5px;
            color:white;

        }
        .custom-img-upload-button:hover {
            background-color: #6d83c3; /* Your custom color */
        }
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, form_target, label):
        return {
            "form_target": form_target,
            "label": label,
        }