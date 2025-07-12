
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image, Service
from users.models import FeatureFlag, Credit
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
    
    def test_post_invalid_form_if_no_credits(self):
        """Test that the form is invalid if the user has no credits"""
        Credit.objects.create(user=self.user, total=0)
        self.user.featureflag_set.create(name='show_credits', enabled=True)
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Create form data with non-English text
        data = {
            'prompt': 'Cat fighting with a dog',  # Russian: 'Cat fighting with a dog'
            'confirm_your_a_human': 'on',
            'bot_field': ''
        }

        # Submit the form with non-English prompt
        response = self.client.post(self.url, data=data)

        # Check that the response indicates an error
        self.assertEqual(response.status_code, 400)

    def test_post_valid_form_when_user_has_credits(self):
        """Test that form is valid if the user has credits"""
        Credit.objects.create(user=self.user, total=10)
        self.user.featureflag_set.create(name='show_credits', enabled=True)
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Create form data with non-English text
        data = {
            'prompt': 'Cat fighting with a dog',
            'confirm_your_a_human': 'on',
            'bot_field': ''
        }

        # Submit the form with non-English prompt
        response = self.client.post(self.url, data=data)

        # Check that the response indicates an error
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
        self.processed_url = reverse('images:process_service', args=[2, self.processed_image.id])
        self.unprocessed_url = reverse('images:process_service', args=[2, self.unprocessed_image.id])

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
        # check a 286 is returned for when a image is processed
        self.assertEqual(response.status_code, 286)
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
        self.assertTrue(Image.objects.exists())

        # Method 1: Get most recent image
        created_image = Image.objects.latest('created')

        # Method 2: Filter by image filename (alternative)
        # created_image = Image.objects.filter(image__contains='test_image.jpg').first()

        # Check that the task was called with the new image ID
        mock_task.assert_called_once_with(created_image.id)

        # Additional check: Verify the exact URL of the new image is in the response
        new_url = reverse('images:process_service', args=[2, created_image.id])
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


class AvatarCreationViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

        # Create avatar creation service
        self.avatar_service = Service.objects.create(
            name='Avatar Creation',
            code=9,
            description='Transform your photo into a stylized AI avatar',
            free=False,
            tokens=5
        )

        # Create test image
        self.test_image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        self.test_image = SimpleUploadedFile(
            name='test_image.gif',
            content=self.test_image_content,
            content_type='image/gif'
        )

        # Create processed and unprocessed avatar images in the database
        self.processed_avatar = Image.objects.create(
            user=self.user,
            image='test_avatar_processed.jpg',
            processed=True
        )

        self.unprocessed_avatar = Image.objects.create(
            user=self.user,
            image='test_avatar_unprocessed.jpg',
            processed=False
        )

        # Create the client and URLs
        self.client = Client()
        self.url = reverse('images:create_avatar')
        self.processed_url = reverse('images:process_service', args=[9, self.processed_avatar.id])
        self.unprocessed_url = reverse('images:process_service', args=[9, self.unprocessed_avatar.id])

    def test_login_required(self):
        """Test that the avatar creation view requires login"""
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('custom_users:login')}?next={self.url}"
        )

    def test_get_request_shows_upload_form(self):
        """Test that GET request shows the avatar upload form"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/create_avatar.html')
        self.assertIn('post_url', response.context)
        self.assertEqual(response.context['post_url'], self.url)

    def test_get_with_processed_avatar_id(self):
        """Test that GET with a processed avatar ID shows the processed avatar"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.processed_url)
        response_content = response.content.decode('utf-8')
        
        # Check a 286 is returned for when an avatar is processed
        self.assertEqual(response.status_code, 286)
        self.assertIn(str(self.processed_avatar.id).encode(), response.content)
        self.assertIn(b'<img', response.content)
        self.assertRegex(
            response_content,
            r'<a[^>]*href="[^"]*"[^>]*download="[^"]*"'
        )

    def test_get_with_unprocessed_avatar_id(self):
        """Test that GET with an unprocessed avatar ID shows the processing view"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(self.unprocessed_url)
        response_content = response.content.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        import re
        self.assertRegex(
            response_content,
            r'<div[^>]*hx-get=["\']{0}["\'][^>]*>'.format(re.escape(self.unprocessed_url))
        )

    @patch('images.views.create_avatar.delay')
    def test_post_valid_form_with_sufficient_credits(self, mock_task):
        """Test POST with valid form data and sufficient credits"""
        # Create user with sufficient credits
        Credit.objects.create(user=self.user, total=10)
        self.user.featureflag_set.create(name='show_credits', enabled=True)
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        import tempfile
        from PIL import Image as PILImage
        
        with tempfile.NamedTemporaryFile(suffix='.jpg') as img_file:
            image = PILImage.new('RGB', (100, 100), color='red')
            image.save(img_file, format='JPEG')
            img_file.seek(0)
            test_image = SimpleUploadedFile(
                name='test_avatar.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

        # Create form data with an image
        form_data = {'image': test_image}
        response = self.client.post(self.url, data=form_data)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode('utf-8')
        self.assertTrue(Image.objects.exists())

        # Get the most recent image
        created_avatar = Image.objects.latest('created')

        # Check that the task was called with the new avatar ID
        mock_task.assert_called_once_with(created_avatar.id)

        # Verify the processing URL is in the response
        new_url = reverse('images:process_service', args=[9, created_avatar.id])
        self.assertIn(new_url, response_content)

    def test_post_insufficient_credits(self):
        """Test POST with insufficient credits (less than 5)"""
        # Create user with insufficient credits
        Credit.objects.create(user=self.user, total=3)
        self.user.featureflag_set.create(name='show_credits', enabled=True)
        self.client.login(email='testuser@example.com', password='testpassword123')

        import tempfile
        from PIL import Image as PILImage
        
        with tempfile.NamedTemporaryFile(suffix='.jpg') as img_file:
            image = PILImage.new('RGB', (100, 100), color='red')
            image.save(img_file, format='JPEG')
            img_file.seek(0)
            test_image = SimpleUploadedFile(
                name='test_avatar.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

        # Create form data with an image
        form_data = {'image': test_image}
        response = self.client.post(self.url, data=form_data)

        # Check that the response indicates an error
        self.assertEqual(response.status_code, 400)
        response_content = response.content.decode('utf-8')
        self.assertIn('You need at least 5 credits', response_content)

    def test_post_without_credits_feature_flag(self):
        """Test POST when user doesn't have credits feature flag enabled"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        import tempfile
        from PIL import Image as PILImage
        
        with tempfile.NamedTemporaryFile(suffix='.jpg') as img_file:
            image = PILImage.new('RGB', (100, 100), color='red')
            image.save(img_file, format='JPEG')
            img_file.seek(0)
            test_image = SimpleUploadedFile(
                name='test_avatar.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

        # Create form data with an image
        form_data = {'image': test_image}
        response = self.client.post(self.url, data=form_data)
        
        # Should succeed since credit check is bypassed
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_form(self):
        """Test POST with invalid form data (no image)"""
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Submit an empty form (should be invalid)
        response = self.client.post(self.url, data={})

        # Check response
        self.assertEqual(response.status_code, 400)

    def test_avatar_service_exists(self):
        """Test that the avatar creation service exists with correct configuration"""
        service = Service.objects.get(code=9)
        self.assertEqual(service.name, 'Avatar Creation')
        self.assertEqual(service.tokens, 5)
        self.assertFalse(service.free)


class AvatarCreationTaskTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

        # Create avatar creation service
        self.avatar_service = Service.objects.create(
            name='Avatar Creation',
            code=9,
            description='Transform your photo into a stylized AI avatar',
            free=False,
            tokens=5
        )

        # Create test image
        self.test_image = Image.objects.create(
            user=self.user,
            image='test_avatar.jpg',
            processed=False
        )

    @patch('images.tasks.requests.post')
    @patch('images.tasks.PILImage.open')
    def test_create_avatar_task_success(self, mock_pil_open, mock_requests_post):
        """Test successful avatar creation task"""
        from images.tasks import create_avatar
        from unittest.mock import Mock
        
        # Mock PIL Image
        mock_image = Mock()
        mock_pil_open.return_value = mock_image
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'fake_avatar_image_data'
        mock_requests_post.return_value = mock_response

        # Execute the task
        create_avatar(self.test_image.id)

        # Verify API was called with correct parameters
        mock_requests_post.assert_called_once()
        call_args = mock_requests_post.call_args
        
        self.assertEqual(call_args[0][0], "https://api.stability.ai/v2beta/stable-image/control/style")
        self.assertIn('authorization', call_args[1]['headers'])
        self.assertIn('Professional avatar portrait', call_args[1]['data']['prompt'])
        self.assertEqual(call_args[1]['data']['strength'], 0.5)

        # Verify image was processed
        self.test_image.refresh_from_db()
        self.assertTrue(self.test_image.processed)

    @patch('images.tasks.requests.post')
    @patch('images.tasks.PILImage.open')
    def test_create_avatar_task_api_failure(self, mock_pil_open, mock_requests_post):
        """Test avatar creation task when API fails"""
        from images.tasks import create_avatar
        from unittest.mock import Mock
        
        # Mock PIL Image
        mock_image = Mock()
        mock_pil_open.return_value = mock_image
        
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_requests_post.return_value = mock_response

        # Execute the task and expect exception
        with self.assertRaises(Exception) as context:
            create_avatar(self.test_image.id)

        self.assertIn('Avatar creation failed', str(context.exception))

        # Verify image was still marked as processed (with error)
        self.test_image.refresh_from_db()
        self.assertTrue(self.test_image.processed)
        self.assertIsNotNone(self.test_image.ai_response)
        self.assertIn('error', self.test_image.ai_response)

    @patch('images.tasks.requests.post')
    @patch('images.tasks.PILImage.open')
    def test_create_avatar_task_with_credits(self, mock_pil_open, mock_requests_post):
        """Test that avatar creation deducts credits correctly"""
        from images.tasks import create_avatar
        from unittest.mock import Mock
        
        # Create user with credits and feature flag
        Credit.objects.create(user=self.user, total=10)
        self.user.featureflag_set.create(name='show_credits', enabled=True)
        
        # Mock PIL Image
        mock_image = Mock()
        mock_pil_open.return_value = mock_image
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'fake_avatar_image_data'
        mock_requests_post.return_value = mock_response

        # Execute the task
        create_avatar(self.test_image.id)

        # Verify credits were deducted
        self.user.credit.refresh_from_db()
        self.assertEqual(self.user.credit.total, 5)  # 10 - 5 = 5


class AvatarServiceIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

        # Create avatar creation service
        self.avatar_service = Service.objects.create(
            name='Avatar Creation',
            code=9,
            description='Transform your photo into a stylized AI avatar',
            free=False,
            tokens=5
        )

        # Create test image
        self.test_image = Image.objects.create(
            user=self.user,
            image='test_avatar.jpg',
            processed=False
        )

        self.client = Client()

    @patch('images.views.create_avatar.delay')
    def test_service_view_avatar_creation(self, mock_task):
        """Test that service view correctly handles avatar creation"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        url = reverse('images:service', args=[9, self.test_image.id])
        response = self.client.get(url)

        # Check that the task was called
        mock_task.assert_called_once_with(self.test_image.id)
        
        # Check response status
        self.assertEqual(response.status_code, 200)

    def test_process_service_view_processed_avatar(self):
        """Test process_service view with processed avatar"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        # Mark image as processed
        self.test_image.processed = True
        self.test_image.save()
        
        url = reverse('images:process_service', args=[9, self.test_image.id])
        response = self.client.get(url)

        # Check that it uses the avatar template
        self.assertEqual(response.status_code, 286)
        response_content = response.content.decode('utf-8')
        self.assertIn('processed-image', response_content)

    def test_process_service_view_unprocessed_avatar(self):
        """Test process_service view with unprocessed avatar"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        
        url = reverse('images:process_service', args=[9, self.test_image.id])
        response = self.client.get(url)

        # Check that it shows processing template
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode('utf-8')
        self.assertIn('processing-image', response_content)

    def test_avatar_url_routing(self):
        """Test that avatar creation URL is properly routed"""
        url = reverse('images:create_avatar')
        self.assertEqual(url, '/create/avatar/')

    def test_avatar_choice_in_services(self):
        """Test that Avatar Creation is available in service choices"""
        from images.models import services
        service_names = [choice[0] for choice in services]
        self.assertIn('Avatar Creation', service_names)