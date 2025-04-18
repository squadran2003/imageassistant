
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image, Service
from images.forms import ImageUploadForm
from unittest.mock import patch
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


class RemoveImageBackgroundViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user =CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

        # Create a test image
        self.test_image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        self.test_image = SimpleUploadedFile(
            name='test_image.gif',
            content=self.test_image_content,
            content_type='image/gif'
        )

        # Create processed and unprocessed images in the database
        self.processed_image = Image.objects.create(
            user=self.user,
            image='test_processed.jpg',
            processed=True
        )

        self.unprocessed_image = Image.objects.create(
            user=self.user,
            image='test_unprocessed.jpg',
            processed=False
        )

        # Create the client and URL
        self.client = Client()
        self.url = reverse('images:remove_image_background')
        self.processed_url = reverse('images:remove_image_background_with_id', args=[self.processed_image.id])
        self.unprocessed_url = reverse('images:remove_image_background_with_id', args=[self.unprocessed_image.id])

    def test_login_required(self):
        """Test that the view requires login"""
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('custom_users:login')}?next={self.url}"
        )

    def test_get_request_shows_upload_form(self):
        """Test that GET request shows the upload form"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/remove_background.html')
        self.assertIn('post_url', response.context)
        self.assertEqual(response.context['post_url'], self.url)

    def test_get_with_processed_image_id(self):
        """Test that GET with a processed image ID shows the processed image"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.processed_url)
        # Convert response to string for easier searching
        response_content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.processed_image.id).encode(), response.content)
        self.assertIn(b'<img', response.content)
        self.assertRegex(
            response_content,
            r'<a[^>]*href="[^"]*"[^>]*download="[^"]*"'
        )

    def test_get_with_unprocessed_image_id(self):
        """Test that GET with an unprocessed image ID shows the processing view"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.unprocessed_url)
        response_content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        import re
        self.assertRegex(
            response_content,
            r'<div[^>]*hx-get=["\']{0}["\'][^>]*>'.format(re.escape(self.unprocessed_url))
        )


    @patch('images.views.remove_background.delay')
    def test_post_valid_form(self, mock_task):
        """Test POST with valid form data"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        import tempfile
        from PIL import Image as PILImage
        test_image = None
        with tempfile.NamedTemporaryFile(suffix='.jpg') as img_file:
            image = PILImage.new('RGB', (100, 100), color='red')
            image.save(img_file, format='JPEG')
            img_file.seek(0)
            test_image = SimpleUploadedFile(
                    name='test_image.jpg',
                    content=img_file.read(),
                    content_type='image/jpeg'
            )

        # Create form data with an image
        form = ImageUploadForm(data={'image': test_image})
        response = self.client.post(self.url, data=form.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode('utf-8')
        import re

        # Check for any hx-get attribute pointing to a background removal URL
        self.assertRegex(
            response_content,
            r'<div[^>]*hx-get=["\'][^"\']*remove/image/background/\d+/["\'][^>]*>'
        )

        # or by filtering on the image name
        self.assertTrue(Image.objects.exists())

        # Method 1: Get most recent image
        created_image = Image.objects.latest('created')

        # Method 2: Filter by image filename (alternative)
        # created_image = Image.objects.filter(image__contains='test_image.jpg').first()

        # Check that the task was called with the new image ID
        mock_task.assert_called_once_with(created_image.id)

        # Additional check: Verify the exact URL of the new image is in the response
        new_url = reverse('images:remove_image_background_with_id', args=[created_image.id])
        self.assertIn(new_url, response_content)

    def test_post_invalid_form_if_not_english(self):
        """Test that non-English prompts are rejected"""
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Create form data with non-English text
        non_english_data = {
            'prompt': 'Кошка дерется с собакой',  # Russian: 'Cat fighting with a dog'
            'confirm_your_a_human': 'on',
            'bot_field': ''
        }

        # Submit the form with non-English prompt
        response = self.client.post(self.url, data=non_english_data)

        # Check that the response indicates an error
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_form(self):
        """Test POST with invalid form data"""
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Submit an empty form (should be invalid)
        response = self.client.post(self.url, data={})

        # Check response
        self.assertEqual(response.status_code, 400)