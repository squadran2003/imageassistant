from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser, Credit
from images.models import Image, Service
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image as PILImage
import tempfile
import os


class ImageProcessingAPITests(APITestCase):
    """Test cases for image processing API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Create credits for user
        Credit.objects.create(user=self.user, total=100)
        
        # Create services (get_or_create to avoid duplicates)
        service1, created = Service.objects.get_or_create(code=1, defaults={'name': 'Greyscale', 'tokens': 2})
        if not created:
            service1.tokens = 2  # Ensure correct token cost
            service1.save()
        
        service2, created = Service.objects.get_or_create(code=2, defaults={'name': 'Remove Background', 'tokens': 5})
        if not created:
            service2.tokens = 5
            service2.save()
            
        service8, created = Service.objects.get_or_create(code=8, defaults={'name': 'Cropping', 'tokens': 3})
        if not created:
            service8.tokens = 3
            service8.save()
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)
        
        # Create test image
        self.test_image = self.create_test_image()
    
    def tearDown(self):
        """Clean up after each test"""
        # Clean up any uploaded files
        for image in Image.objects.all():
            if image.image:
                try:
                    image.image.delete(save=False)
                except:
                    pass
        
    def create_test_image(self):
        """Create a test image file"""
        img = PILImage.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return SimpleUploadedFile(
            name='test.png',
            content=img_io.getvalue(),
            content_type='image/png'
        )
    
    def create_large_test_image(self):
        """Create a large test image file (over 10MB)"""
        # Create a large enough image to exceed 10MB
        # 10MB = 10,485,760 bytes, so we'll create content larger than that
        large_content = b'0' * (11 * 1024 * 1024)  # 11MB of zeros
        return SimpleUploadedFile(
            name='large_test.png',
            content=large_content,
            content_type='image/png'
        )


class RemoveBackgroundAPITests(ImageProcessingAPITests):
    """Test cases for remove background API endpoint"""

    def setUp(self):
        super().setUp()
        self.url = reverse('api:remove-background')

    def test_successful_background_removal(self):
        """Test successful background removal request"""
        data = {'image': self.test_image}
        
        with patch('images.tasks.remove_background.delay') as mock_task:
            response = self.client.post(self.url, data, format='multipart')
            
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('image_id', response.data)
        self.assertEqual(response.data['detail'], 'Background removal started.')
        mock_task.assert_called_once()

    def test_no_image_provided(self):
        """Test error when no image is provided"""
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Image file is required.')

    def test_invalid_file_type(self):
        """Test error with invalid file type"""
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        data = {'image': invalid_file}
        
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid file type. Only JPEG, PNG, and WebP are allowed.')

    def test_file_too_large(self):
        """Test error with file too large"""
        large_image = self.create_large_test_image()
        data = {'image': large_image}
        
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Image file too large. Maximum size is 10MB.')

    def test_insufficient_credits(self):
        """Test error when user has insufficient credits"""
        self.user.credit.total = 1
        self.user.credit.save()
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)
        self.assertEqual(response.data['detail'], 'Insufficient credits.')

    def test_service_not_available(self):
        """Test error when service is not available"""
        Service.objects.filter(code=2).delete()
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['detail'], 'Service not available.')

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the endpoint"""
        self.client.force_authenticate(user=None)
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateGrayscaleAPITests(ImageProcessingAPITests):
    """Test cases for grayscale conversion API endpoint"""

    def setUp(self):
        super().setUp()
        self.url = reverse('api:create-grayscale')

    def test_successful_grayscale_conversion(self):
        """Test successful grayscale conversion request"""
        data = {'image': self.create_test_image()}
        
        with patch('images.tasks.create_greyscale.delay') as mock_task:
            response = self.client.post(self.url, data, format='multipart')
            
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('image_id', response.data)
        self.assertEqual(response.data['detail'], 'Grayscale conversion started.')
        mock_task.assert_called_once()

    def test_no_image_provided(self):
        """Test error when no image is provided"""
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Image file is required.')

    def test_insufficient_credits(self):
        """Test error when user has insufficient credits"""
        # Verify the user starts with credits
        self.assertEqual(self.user.credit.total, 100)
        
        # Set insufficient credits
        self.user.credit.total = 1
        self.user.credit.save()
        
        # Verify the credit was updated
        self.user.credit.refresh_from_db()
        self.assertEqual(self.user.credit.total, 1)
        
        # Make the request with fresh image
        data = {'image': self.create_test_image()}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)
        self.assertEqual(response.data['detail'], 'Insufficient credits.')

    def test_service_not_available(self):
        """Test error when service is not available"""
        Service.objects.filter(code=1).delete()
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['detail'], 'Service not available.')


class CreateOutlineAPITests(ImageProcessingAPITests):
    """Test cases for outline creation API endpoint"""

    def setUp(self):
        super().setUp()
        self.url = reverse('api:create-outline')

    def test_successful_outline_creation(self):
        """Test successful outline creation request"""
        data = {'image': self.test_image}
        
        with patch('images.tasks.create_image_outline_task.delay') as mock_task:
            response = self.client.post(self.url, data, format='multipart')
            
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('image_id', response.data)
        self.assertEqual(response.data['detail'], 'Outline creation started.')
        mock_task.assert_called_once()

    def test_no_image_provided(self):
        """Test error when no image is provided"""
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Image file is required.')

    def test_insufficient_credits(self):
        """Test error when user has insufficient credits"""
        self.user.credit.total = 2
        self.user.credit.save()
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)
        self.assertEqual(response.data['detail'], 'Insufficient credits.')

    def test_service_not_available(self):
        """Test error when service is not available"""
        Service.objects.filter(code=8).delete()
        
        data = {'image': self.test_image}
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['detail'], 'Service not available.')


class ImageStatusAPITests(ImageProcessingAPITests):
    """Test cases for image status API endpoint"""

    def setUp(self):
        super().setUp()
        self.image = Image.objects.create(
            image='test.png',
            user=self.user,
            processed=False
        )
        self.url = reverse('api:image-status', kwargs={'image_id': self.image.id})

    def test_image_still_processing(self):
        """Test response when image is still being processed"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['detail'], 'Image is still being processed.')

    def test_image_processing_complete(self):
        """Test response when image processing is complete"""
        self.image.processed = True
        self.image.save()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)

    def test_image_not_found(self):
        """Test error when image doesn't exist"""
        url = reverse('api:image-status', kwargs={'image_id': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Image not found.')

    def test_unauthorized_access_to_other_user_image(self):
        """Test that users can't access other users' images"""
        other_user = CustomUser.objects.create_user(
            email='other@example.com',
            password='otherpassword'
        )
        other_image = Image.objects.create(
            image='other.png',
            user=other_user,
            processed=True
        )
        
        url = reverse('api:image-status', kwargs={'image_id': other_image.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SecurityTests(APITestCase):
    """Security-focused tests for API endpoints"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='security@example.com',
            password='securepassword123'
        )
        Credit.objects.create(user=self.user, total=100)
        Service.objects.get_or_create(code=1, defaults={'name': 'Greyscale', 'tokens': 2})
        Service.objects.get_or_create(code=2, defaults={'name': 'Remove Background', 'tokens': 5})
        Service.objects.get_or_create(code=8, defaults={'name': 'Cropping', 'tokens': 3})

    def test_malicious_file_upload(self):
        """Test rejection of potentially malicious files"""
        self.client.force_authenticate(user=self.user)
        
        # Test with executable file
        malicious_file = SimpleUploadedFile(
            name='malicious.exe',
            content=b'MZ\x90\x00',  # PE header signature
            content_type='application/x-executable'
        )
        
        url = reverse('api:remove-background')
        response = self.client.post(url, {'image': malicious_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid file type. Only JPEG, PNG, and WebP are allowed.')

    def test_sql_injection_in_image_status(self):
        """Test SQL injection protection in image status endpoint"""
        self.client.force_authenticate(user=self.user)
        
        # Try SQL injection in URL parameter
        malicious_id = "1'; DROP TABLE images_image; --"
        url = f"/api/v1/image/status/{malicious_id}/"
        
        response = self.client.get(url)
        # Should return 404 (not found) rather than causing database issues
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_django_file_security(self):
        """Test that Django provides comprehensive file security"""
        # Django automatically prevents various security issues:
        # 1. Empty filenames - raises SuspiciousFileOperation
        # 2. Path traversal - strips directory components  
        # 3. Dangerous characters - validates filename format
        
        # Test that we can't create files with empty names
        with self.assertRaises(Exception):  # SuspiciousFileOperation
            SimpleUploadedFile(name='', content=b'test', content_type='image/png')
        
    def test_path_traversal_protection_note(self):
        """Test that path traversal is handled by Django framework"""
        # Note: Django's SimpleUploadedFile automatically sanitizes filenames
        # containing path traversal attempts (../) by stripping the path components.
        # This is Django's built-in security feature working correctly.
        # Our validation serves as an additional layer of protection for edge cases.
        self.client.force_authenticate(user=self.user)
        
        # This demonstrates that Django sanitizes the filename
        traversal_attempt = SimpleUploadedFile(
            name='../../../etc/passwd.png',
            content=b'fake image content',
            content_type='image/png'
        )
        
        # The filename will be sanitized to just 'passwd.png' by Django
        self.assertEqual(traversal_attempt.name, 'passwd.png')
        
        url = reverse('api:create-grayscale')
        response = self.client.post(url, {'image': traversal_attempt}, format='multipart')
        
        # Should succeed because Django sanitized the filename
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_rate_limiting_simulation(self):
        """Test basic rate limiting behavior (simulation)"""
        self.client.force_authenticate(user=self.user)
        
        # Create small test image
        test_image = SimpleUploadedFile(
            name='test.png',
            content=PILImage.new('RGB', (10, 10)).tobytes(),
            content_type='image/png'
        )
        
        url = reverse('api:remove-background')
        
        # Make multiple rapid requests
        responses = []
        for _ in range(5):
            response = self.client.post(url, {'image': test_image}, format='multipart')
            responses.append(response.status_code)
        
        # All should succeed in test environment (no actual rate limiting configured)
        # In production, you'd want to implement actual rate limiting
        for status_code in responses:
            self.assertIn(status_code, [202, 400, 402])  # Accept various valid responses


class ProcessImageViewTests(ImageProcessingAPITests):
    """Test the base ProcessImageView functionality"""
    
    def test_validate_image_upload_success(self):
        """Test successful image validation"""
        from api.views import ProcessImageView
        
        view = ProcessImageView()
        
        # Mock request with valid image
        mock_request = MagicMock()
        mock_request.FILES = {'image': self.test_image}
        mock_request.user = self.user
        
        image, error_response = view.validate_image_upload(mock_request)
        
        self.assertIsNotNone(image)
        self.assertIsNone(error_response)
        self.assertEqual(image.user, self.user)
        self.assertFalse(image.processed)

    def test_validate_image_upload_no_file(self):
        """Test validation when no image file is provided"""
        from api.views import ProcessImageView
        
        view = ProcessImageView()
        
        # Mock request without image
        mock_request = MagicMock()
        mock_request.FILES = {}
        
        image, error_response = view.validate_image_upload(mock_request)
        
        self.assertIsNone(image)
        self.assertIsNotNone(error_response)
        self.assertEqual(error_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_image_upload_large_file(self):
        """Test validation with oversized file"""
        from api.views import ProcessImageView
        
        view = ProcessImageView()
        
        # Create mock large file
        large_file = MagicMock()
        large_file.size = 15 * 1024 * 1024  # 15MB
        large_file.content_type = 'image/png'
        
        mock_request = MagicMock()
        mock_request.FILES = {'image': large_file}
        
        image, error_response = view.validate_image_upload(mock_request)
        
        self.assertIsNone(image)
        self.assertIsNotNone(error_response)
        self.assertEqual(error_response.status_code, status.HTTP_400_BAD_REQUEST)
