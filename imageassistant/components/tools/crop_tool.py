from django_components import Component, register, types


@register("crop_tool")
class CropTool(Component):

    template_name = "crop_tool.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, img_url, form, service_id, image_id, token):
        return {
            "img_url": img_url,
            "form": form,
            "service_id": service_id,
            "image_id": image_id,
            "token": token
        }

    js: types.js = """
        (function(){
            const image = document.getElementById('cropping-image');
            const cropForm = document.getElementById('crop-form');
            const x = document.getElementById('id_x');
            const y = document.getElementById('id_y');
            const width = document.getElementById('id_width');
            const height = document.getElementById('id_height');
            image.style.display = 'block';
            const cropper = new Cropper(image, {
                aspectRatio: 16 / 9,
                crop: function (event) {
                    x.value = event.detail.x;
                    y.value = event.detail.y;
                    width.value = event.detail.width;
                    height.value = event.detail.height;
                }
            });
        })()
    """
