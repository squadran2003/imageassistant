from django_components import Component, register, types

@register("main_content")
class MainContent(Component):

    template = """
            {% load static %}
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
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                     <div class="card custom-card">
                        <div class="card-image">
                            <div class="response-video">
                                <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/greyscale_video_thumbnail.png' %}">
                                    <source src="{{MEDIA_URL}}video/image_assistant_greyscale_video.mp4" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                        <div class="card-content">
                            <span class="card-title">Black & White Conversion</span>
                            <p>Transform your images into classic black-and-white using advanced grayscale techniques. This service is perfect for adding a timeless, artistic feel to photos or preparing images for use in documents, presentations, or websites where a monochrome aesthetic is preferred.

                            </p>
                            <p><strong>Price:</strong> Free</p>
                        </div>
                    </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card">
                        <div class="card-image">
                            <div class="response-video">
                                <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/image_enhancement.png' %}">
                                    <source src="{{MEDIA_URL}}video/image_assistant_image_enhance_video.mp4" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                        <div class="card-content">
                            <span class="card-title">Image Enhancement</span>
                            <p>This service enhances your image using AI. It enhances the image resolution by 4x using predictive and generative AI. Ideal for enhancing the quality of compressed images.

                            </p>
                            <p><strong>Price:</strong> $3</p>
                        </div>
                    </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card">
                            <div class="card-image">
                                <div class="response-video">
                                    <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/remove_background.png' %}">
                                        <source src="{{MEDIA_URL}}video/remove_background_demo.mp4" type="video/mp4">
                                        Your browser does not support the video tag.
                                    </video>
                                </div>
                            </div>
                            <div class="card-content">
                                <span class="card-title">Remove Background</span>
                                <p>This service removes a image background using AI.

                                </p>
                                <p><strong>Price:</strong>$5</p>
                            </div>
                    </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                     <div class="card custom-card">
                        <div class="card-image">
                            <div class="response-video">
                                <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/thumbnail.png' %}">
                                    <source src="{{MEDIA_URL}}video/remove_background_demo.mp4" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                        <div class="card-content">
                            <span class="card-title">Thumbnail Generation</span>
                            <p>This service takes your image and resizes it to a thumbnail size.

                            </p>
                            <p><strong>Price:</strong> FREE</p>
                        </div>
                    </div>
                </div>
                 <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card">
                        <div class="card-image">
                            <div class="response-video">
                                <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/crop_images.png' %}">
                                    <source src="{{MEDIA_URL}}video/image_assistant_cropping_video.mp4" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                        <div class="card-content">
                            <span class="card-title">Image Cropping</span>
                            <p>This service provides a tool that allows you to crop your image to a specified size.

                            </p>
                            <p><strong>Price:</strong> FREE</p>
                        </div>
                    </div>
                </div>
                 <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card">
                        <div class="card-image">
                            <div class="response-video">
                                <video controls style="max-width:100%; min-height:100%" poster="{% static 'img/resizing.png' %}">
                                    <source src="{{MEDIA_URL}}video/remove_background_demo.mp4" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                            </div>
                        </div>
                        <div class="card-content">
                            <span class="card-title">Resizing</span>
                            <p>Ensure your images fit perfectly for any platform with our high-quality resizing service. We can resize images to specified dimensions while maintaining optimal clarity and resolution.
                            Attention! a small image when resized to a larger size may lose quality, in this case try our Image Enhancement service.

                            </p>
                            <p><strong>Price:</strong> FREE</p>
                        </div>
                    </div>
                </div>
            </div>
    """

    def get_context_data(self, form, media_url):
        return {
            "form": form,
            "MEDIA_URL":  media_url
        }
