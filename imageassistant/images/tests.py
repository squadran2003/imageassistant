
from django.test import TestCase
from django.urls import reverse
from .views import generate_image
from .models import Image, Service
from freezegun import freeze_time
from datetime import datetime
from users.models import CustomUser


class CreateImageViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@test.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_login(self.user)
        self.url = reverse('images:generate_image')
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
        Service.objects.create(name='GenerateImage', code=7)


    def test_create_image_without_prompt(self):
        session = self.client.session
        session.save()
        data = self.valid_data.copy()
        data['prompt'] = ''
        data['confirm_your_a_human'] = 'on'
        data['bot_field'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
    

    def test_create_image_with_bot_field_filled(self):
        session = self.client.session
        session.save()
        data = self.valid_data.copy()
        data['bot_field'] = 'bot'
        data['confirm_your_a_human'] = 'on'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
    
    def test_create_image_without_confirm_bot_field_return_error(self):
        session = self.client.session
        session.save()
        data = self.valid_data.copy()
        data['prompt'] = 'Cat fighting'
        data['confirm_your_a_human'] = ''
        data['bot_field'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
    

    def test_create_image_success_gets_form_that_fires_on_load(self):
        session = self.client.session
        session.save()
        data = self.valid_data.copy()
        data['prompt'] = 'Cat fighting'
        data['confirm_your_a_human'] = 'on'
        data['bot_field'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)