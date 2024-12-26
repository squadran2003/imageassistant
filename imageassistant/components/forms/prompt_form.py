from django_components import Component, register, types

@register("prompt_form")
class PromptForm(Component):
    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, **kwargs):
        return {
            "attrs": kwargs.get("attrs", {}),
            "errors": kwargs.get("errors", []),
            "django_form": kwargs.get("form", None),
        }

    template: types.django_html = """
        {% component_css_dependencies %}
         <div class="row mt-5">
            <div class="col s12 m12 lg12">
                <form {% html_attrs attrs %}>
                    {% for field in django_form %}
                        <div class="input-field col s12 m12 lg12">
                            {% if field.errors %}
                                <span class="helper-text" id="error">{{ field.errors }}</span>
                            {% endif %}
                            {{ field }}
                            {{ field.help_text }}
                            {% for error in field.errors %}
                                <span class="helper-text" id="error">{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% endfor %}
                    <a  onclick="htmx.trigger('#prompt-form', 'submit')" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;"></span>Submit</a>
                </form>
            </div>
        </div>
    """

    css: types.css = """
        .prompt-form{
            min-width: 100%;
        }
        #id_prompt{
            color: white;
        }
        .input-field {
            color: white;
        }
        #error{
            color: red;
        }
    """
