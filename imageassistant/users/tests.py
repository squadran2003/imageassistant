from django.test import TestCase, Client
from django.urls import reverse
from .forms import CustomUserForm
from users.models import CustomUser


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

    # def test_signup_post_invalid_when_password_dont_match(self):
    #     data = {
    #         'first_name': 'Test',
    #         'last_name': 'User',
    #         'password1': 'password123',
    #         'password2': 'password12',
    #         'email': 'testuser@example.com'
    #     }
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 400)

    # def test_signup_post_invalid_when_email_not_valid(self):
    #     data = {
    #         'first_name': 'Test',
    #         'last_name': 'User',
    #         'password1': 'password123',
    #         'password2': 'password123',
    #         'email': 'testuserexample.com'
    #     }
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 400)
