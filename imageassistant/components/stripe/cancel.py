from django_components import Component, register, types

@register("cancel")
class Cancel(Component):

    template: types.django_html = """
       <html>
            <head>
            <title>Checkout canceled</title>
            <link rel="stylesheet" href="style.css">
            </head>
            <body>
            <section>
                <p>Forgot to add something to your cart? Shop around then come back to pay!</p>
            </section>
            </body>
        </html>

    """


    def get_context_data(self, url, label):
        return {
            "url": url,
            "label": label
        }