from django_components import Component, register, types

@register("main_content")
class MainContent(Component):

    template = """
            <div class="row">
                <div class="col s12">
                        <div class="row">
                            <div class="col s12 m12 l12 x12">
                                <div class="banner-text">
                                    <h1 class="banner">Unlock Your Image's Full Potential</h1>
                                    <p>Transform and Enhance your images with ImageAssistant's services powered by AI.
                                        Start creating stunning visuals in just a few clicks!
                                    </p>
                                </div>
                                {% component "upload_component" id="upload-form" target="#content" swap="innerHTML"  url="images:add" form="{{form}}" %}{% endcomponent %}
                            </div>
                        </div>
                </div>
            </div>
            <div class="row">
                <div class="col s12 xs12 m12 l12 x12">
                    <h2 class="center text">Services Offered</h2>
                </div>
            </div>
            <div class="row">
                {% for service in services %}
                    <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                        <div class="card custom-card">
                            <div class="card-image">
                                <div class="response-video">
                                    <video controls style="max-width:100%; min-height:100%" poster="{{service.poster_path}}" loading="lazy">
                                        <source src="{{service.video_path}}" type="video/mp4">
                                        Your browser does not support the video tag.
                                    </video>
                                </div>
                            </div>
                            <div class="card-content">
                                <span class="card-title">{{service.name}}</span>
                                <p>{{service.description|safe}}

                                </p>
                                {% if service.free %}
                                    <p><strong>Price:</strong> Free</p>
                                {% else %}
                                    <p><strong>Price:</strong> ${{service.cost}}</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                {% endfor %}
                
            </div>
    """

    def get_context_data(self, form, services=[]):
        return {
            "form": form,
            "services": services
        }
