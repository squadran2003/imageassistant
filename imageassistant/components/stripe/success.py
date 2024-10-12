from django_components import Component, register, types

@register("success")
class Success(Component):

    template: types.django_html = """
       <!DOCTYPE html>
        <html>
        <head>
        <title>Thanks for your order!</title>
        <link rel="stylesheet" href="style.css">
        </head>
        <body>
        <section>
            <p>
            We appreciate your business! If you have any questions, please email
            <a href="mailto:orders@example.com">orders@example.com</a>.
            </p>
        </section>
        </body>
        </html>

    """



    def get_context_data(self, url, label):
        return {
            "url": url,
            "label": label
        }