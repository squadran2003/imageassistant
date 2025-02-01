from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from .views import create_image
from .models import Image

class CreateImageViewTests(TestCase):
    def setUp(self):
        self.url = reverse('images:create_image')
        self.invalid_propmpt = """
                Contrary to popular belief, Lorem Ipsum is not simply random text. 
                It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, 
                a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, 
                from a Lorem Ipsum passage, and going through the cites of the word in classical literature, 
                discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

                The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.            

        """
        self.valid_data = {
            'prompt': "cat fighting",
            'bot_field': '',
        }
        self.maxDiff = None

    def test_create_image_with_prompt_but_too_long(self):
        data = self.valid_data.copy()
        data['prompt'] = self.invalid_propmpt
        response = self.client.post(self.url, data)
        expected_response = """
            <form hx-post="/images/create/image/" hx-target=this hx-swap="outerHTML" id="prompt-form" class="bg-[#262c3d] shadow-md rounded px-8 pt-6 pb-8 mb-4 mt-1">
                <input type="hidden" name="csrfmiddlewaretoken" value="5YPcGRcCcYrNASX7X4yiPeEzKZuTViRzF45fdmEogXQ2PpozVY5x489HXzmPQZ5j">
                <label for="id_bot_field">Bot field:</label>
                <input type="hidden" name="bot_field" class="validate" id="id_bot_field">
                <label for="id_prompt">Prompt:</label>
                <textarea name="prompt" cols="40" rows="5" class="shadow appearance-none border rounded mt-2 min-h-50 mb-2 p-2 w-full text-gray-700 focus:outline-none focus:shadow-outline required:border-red-500" placeholder="Tell us more about the image you want to generate" style="resize:none;" required id="id_prompt">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of &quot;de Finibus Bonorum et Malorum &quot;(The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, &quot;Lorem ipsum dolor sit amet..&quot;, comes from a line in section 1.10.32.

            The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from &quot;de Finibus Bonorum et Malorum &quot;by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.</textarea>
                <div class="text-red-700 px-4 py-3 rounded relative bg-[#c9aab6] text-sm">
                    <ul class="errorlist">
                        <li>Prompt must be less than 20 characters</li>
                    </ul>
                </div>
                <button type="submit" onclick="htmx.trigger('#prompt-form', 'submit')" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium  text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" id="prompt-button">
                    <div class="hidden htmx-indicator progress" id="indicator">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </div>
                    <span id="prompt-progress-text">Submit</span>
                </button>
            </form>        
        """
        self.assertHTMLEqual(response.content.decode(), expected_response)
    
    def test_create_image_without_prompt(self):
        data = self.valid_data.copy()
        data['prompt'] = ''
        response = self.client.post(self.url, data)
        expected_response = """
            <form hx-post="/images/create/image/" hx-target=this hx-swap="outerHTML" id="prompt-form" class="bg-[#262c3d] shadow-md rounded px-8 pt-6 pb-8 mb-4 mt-1">
                <input type="hidden" name="csrfmiddlewaretoken" value="5YPcGRcCcYrNASX7X4yiPeEzKZuTViRzF45fdmEogXQ2PpozVY5x489HXzmPQZ5j">
                <label for="id_bot_field">Bot field:</label>
                <input type="hidden" name="bot_field" class="validate" id="id_bot_field">
                <label for="id_prompt">Prompt:</label>
                <textarea name="prompt" cols="40" rows="5" class="shadow appearance-none border rounded mt-2 min-h-50 mb-2 p-2 w-full text-gray-700 focus:outline-none focus:shadow-outline required:border-red-500" placeholder="Tell us more about the image you want to generate" style="resize:none;" required id="id_prompt">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of &quot;de Finibus Bonorum et Malorum &quot;(The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, &quot;Lorem ipsum dolor sit amet..&quot;, comes from a line in section 1.10.32.

            The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from &quot;de Finibus Bonorum et Malorum &quot;by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.</textarea>
                <div class="text-red-700 px-4 py-3 rounded relative bg-[#c9aab6] text-sm">
                    <ul class="errorlist">
                        <li>Prompt is required</li>
                    </ul>
                </div>
                <button type="submit" onclick="htmx.trigger('#prompt-form', 'submit')" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium  text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" id="prompt-button">
                    <div class="hidden htmx-indicator progress" id="indicator">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </div>
                    <span id="prompt-progress-text">Submit</span>
                </button>
            </form>        
        """
        self.assertHTMLEqual(response.content.decode(), expected_response)

    def test_create_image_with_bot_field_filled(self):
        data = self.valid_data.copy()
        data['bot_field'] = 'bot'
        response = self.client.post(self.url, data)
        expected_response = """
            <form hx-post="/images/create/image/" hx-target=this hx-swap="outerHTML" id="prompt-form" class="bg-[#262c3d] shadow-md rounded px-8 pt-6 pb-8 mb-4 mt-1">
                <input type="hidden" name="csrfmiddlewaretoken" value="5YPcGRcCcYrNASX7X4yiPeEzKZuTViRzF45fdmEogXQ2PpozVY5x489HXzmPQZ5j">
                <label for="id_bot_field">Bot field:</label>
                <input type="hidden" name="bot_field" class="validate" id="id_bot_field">
                <label for="id_prompt">Prompt:</label>
                <textarea name="prompt" cols="40" rows="5" class="shadow appearance-none border rounded mt-2 min-h-50 mb-2 p-2 w-full text-gray-700 focus:outline-none focus:shadow-outline required:border-red-500" placeholder="Tell us more about the image you want to generate" style="resize:none;" required id="id_prompt">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of &quot;de Finibus Bonorum et Malorum &quot;(The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, &quot;Lorem ipsum dolor sit amet..&quot;, comes from a line in section 1.10.32.

            The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from &quot;de Finibus Bonorum et Malorum &quot;by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.</textarea>
                <div class="text-red-700 px-4 py-3 rounded relative bg-[#c9aab6] text-sm">
                    <ul class="errorlist">
                        <li>Invalid request</li>
                    </ul>
                </div>
                <button type="submit" onclick="htmx.trigger('#prompt-form', 'submit')" class="mt-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium  text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" id="prompt-button">
                    <div class="hidden htmx-indicator progress" id="indicator">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </div>
                    <span id="prompt-progress-text">Submit</span>
                </button>
            </form>        
        """
        self.assertHTMLEqual(response.content.decode(), expected_response)

    def test_create_image_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('images:service', args=[7, Image.objects.first().id]))
