from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.conf import settings
from unittest.mock import patch, Mock
from .forms import CustomUserForm, AddCreditForm
from users.models import CustomUser, Credit
from .forms import CustomUserForm


class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('custom_users:signup')

    def test_signup_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserForm)

    def test_signup_post_valid(self):
        data = {
            'password': 'password123',
            'confirm_password': 'password123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.filter(email=data['email']).exists())

    def test_signup_post_invalid_when_password_dont_match(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password12',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_signup_post_invalid_when_email_not_valid(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuserexample.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

class TestDeleteUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="test@test.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.login(
            email="test@test.com",
            password="password123"
        )
        self.url = reverse('custom_users:delete', args=[self.user.id])

    def test_view_deletes_user(self):
        self.client.get(reverse('custom_users:delete', args=[self.user.id]))
        self.assertEqual(CustomUser.objects.filter(id=self.user.id).count(), 0)


class TestAddCreditView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="test@test.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.login(
            email="test@test.com",
            password="password123"
        )
        self.url = reverse('custom_users:add-credit')

    def test_get_add_credit_view(self):
        """Test GET request renders correct template and form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_credit.html')
        self.assertIsInstance(response.context['form'], AddCreditForm)
        self.assertEqual(response.context['user'], self.user)

    def test_add_credit_creates_new_credit_record(self):
        """Test adding credit creates new Credit record if none exists"""
        data = {'amount': 10.00}
        response = self.client.post(self.url, data)
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Check credit was created
        credit = Credit.objects.get(user=self.user)
        expected_amount = 500
        self.assertEqual(credit.total, expected_amount)
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(f"${expected_amount} credit added successfully", str(messages[0]))

    # def test_add_credit_updates_existing_credit_record(self):
    #     """Test adding credit updates existing Credit record"""
    #     # Create existing credit record
    #     Credit.objects.create(user=self.user, total=50.00)
        
    #     data = {'amount': 25.00}
    #     response = self.client.post(self.url, data)
        
    #     # Check redirect
    #     self.assertEqual(response.status_code, 302)
        
    #     # Check credit was updated
    #     credit = Credit.objects.get(user=self.user)
    #     expected_additional = settings.CREDIT_SETTINGS * 25.00
    #     self.assertEqual(credit.total, 50.00 + expected_additional)

    # def test_add_credit_with_decimal_amount(self):
    #     """Test adding credit with decimal amounts"""
    #     data = {'amount': 15.75}
    #     response = self.client.post(self.url, data)
        
    #     self.assertEqual(response.status_code, 302)
        
    #     credit = Credit.objects.get(user=self.user)
    #     expected_amount = settings.CREDIT_SETTINGS * 15.75
    #     self.assertEqual(credit.total, expected_amount)

    # def test_add_credit_invalid_form(self):
    #     """Test form validation with invalid data"""
    #     data = {'amount': -5.00}  # Negative amount should be invalid
    #     response = self.client.post(self.url, data)
        
    #     # Should not redirect (form invalid)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'form', 'amount', None)  # Check for form errors
        
    #     # Credit should not be created
    #     self.assertFalse(Credit.objects.filter(user=self.user).exists())

    # def test_add_credit_empty_amount(self):
    #     """Test form validation with empty amount"""
    #     data = {'amount': ''}
    #     response = self.client.post(self.url, data)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Credit.objects.filter(user=self.user).exists())

    # def test_add_credit_zero_amount(self):
    #     """Test form validation with zero amount"""
    #     data = {'amount': 0.00}
    #     response = self.client.post(self.url, data)
        
    #     # Depending on your form validation, this might be invalid
    #     # Adjust assertion based on your form's min_value setting
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Credit.objects.filter(user=self.user).exists())

    # def test_add_credit_requires_authentication(self):
    #     """Test that unauthenticated users cannot access the view"""
    #     self.client.logout()
    #     response = self.client.get(self.url)
        
    #     # Should redirect to login
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    # def test_add_credit_large_amount(self):
    #     """Test adding large credit amounts"""
    #     data = {'amount': 999.99}
    #     response = self.client.post(self.url, data)
        
    #     self.assertEqual(response.status_code, 302)
        
    #     credit = Credit.objects.get(user=self.user)
    #     expected_amount = settings.CREDIT_SETTINGS * 999.99
    #     self.assertEqual(credit.total, expected_amount)

    # def test_credit_calculation_with_settings(self):
    #     """Test that credit calculation uses CREDIT_SETTINGS correctly"""
    #     # Mock CREDIT_SETTINGS value for this test
    #     with self.settings(CREDIT_SETTINGS=2):
    #         data = {'amount': 10.00}
    #         response = self.client.post(self.url, data)
            
    #         credit = Credit.objects.get(user=self.user)
    #         self.assertEqual(credit.total, 20.00)  # 10.00 * 2
