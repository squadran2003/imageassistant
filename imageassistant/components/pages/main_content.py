from django_components import Component, register, types

@register("main_content")
class MainContent(Component):

    template = """
            <div class="row">
                <div class="col s12">
                    <div id="main-banner">
                        <div class="row">
                            <div class="col s12 m12 l12 x12">
                                <div class="banner-text">
                                    <h1 class="banner">Unlock Your Image's Full Potential</h1>
                                    <h5>Transform, Enhance, and Personalize your images with ImageAssistant's powerful tools.
                                        Start creating stunning visuals in just a few clicks!
                                    </h5>
                                </div>
                                {% component "upload_component" id="upload-form" target="#content" swap="innerHTML"  url="images:add" form="{{form}}" %}{% endcomponent %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col s12 xs12 m12 l12 x12" style="margin-bottom: 50px;">
                    <h2 class="center">Services Offered</h2>
                </div>
            </div>
            <div class="row">
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                <div class="card custom-card-height">
                    <div class="card-image">
                    <span class="card-title" style="color:black">Black & White Conversion</span>
                    </div>
                    <div class="card-content">
                    <p>Transform your images into classic black-and-white using advanced grayscale techniques with Pillow, a powerful Python library. This service is perfect for adding a timeless, artistic feel to photos or preparing images for use in documents, presentations, or websites where a monochrome aesthetic is preferred.

                    </p>
                    <p><strong>Price:</strong> Free</p>
                    </div>
                </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card-height">
                        <div class="card-image">
                            <span class="card-title" style="color:black">Resizing</span>
                        </div>
                        <div class="card-content">
                            <p>Ensure your images fit perfectly for any platform with our high-quality resizing service.
                                Using the Pillow library, we can resize images to specified dimensions while maintaining optimal clarity and resolution.
                                Attention! a small image when resized to a larger size may lose quality.
                            </p>
                            <p><strong>Price:</strong> Free</p>
                        </div>
                    </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card-height">
                        <div class="card-image">
                            <span class="card-title" style="color:black">Create Thumbnail</span>
                        </div>
                        <div class="card-content">
                            <p>This service takes your image and resizes it to a thumbnail size.
                            </p>
                            <p><strong>Price:</strong>Free</p>
                        </div>
                    </div>
                </div>
                <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card-height">
                        <div class="card-image">
                            <span class="card-title" style="color:black">Image Cropping</span>
                        </div>
                        <div class="card-content">
                            <p>This service provides a tool that allows you to crop your image to a specified size.
                            </p>
                            <p><strong>Price:</strong>Free</p>
                        </div>
                    </div>
                </div>
                 <div class="col s12 xs12 m4 l4" style="margin-top: 50px;">
                    <div class="card custom-card-height">
                        <div class="card-image">
                            <span class="card-title" style="color:black">Image Enhancement</span>
                        </div>
                        <div class="card-content">
                            <p>This service enhances your image using Stability AI. It enhances the image resolution by 4x using predictive and generative AI.
                            Ideal for enhancing the quality of compressed images.
                            </p>
                            <p><strong>Price:</strong>$2</p>
                        </div>
                    </div>
                </div>
            </div>
    """

    def get_context_data(self, form):
        return {
            "form": form,
        }
