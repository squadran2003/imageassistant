from django_components import Component, register, types

@register("processed_image_page")
class ProcessedImagePage(Component):

    template = """
        <div class="row">
                <div class="col s12 m12 l12 xl12">
                    {% if file.alternate_url %}
                        <a href="{{ file.alternate_url }}"  download="{{ file.alternate_url }}" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;margin-top:5px;">download</span>Download</a>
                    {% else %}
                        <a href="{{ file.image.url }}" download="{{ file.image.url }}" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;margin-top:5px;">download</span>Download</a>
                    {% endif %}   
                </div>
            </div>
            <div class="row">
                <div class="col s12 m12 l12 xl12">
                    {% if file.alternate_url %}
                        <img src="{{ file.alternate_url }}" alt="Processed Image" class="responsive-img">
                    {% else %}
                        <img src="{{ file.image.url }}" alt="Processed Image" class="responsive-img">
                    {% endif %}
                </div>
            </div>
    """

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, file):
        return {
           "file": file

        }
