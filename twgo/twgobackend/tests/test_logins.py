from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='password')
        self.super_admin = User.objects.create_superuser(email='superadmin@example.com', password='password')

    def test_login_custom_user(self):
        url = reverse('userlogin')
        data = {'email': 'user@example.com', 'password': 'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_custom_user_invalid_credentials(self):
        url = reverse('userlogin')
        data = {'email': 'user@example.com', 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_custom_admin(self):
        url = reverse('adminlogin')
        data = {'email': 'admin@example.com', 'password': 'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_custom_admin_invalid_credentials(self):
        url = reverse('adminlogin')
        data = {'email': 'admin@example.com', 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_custom_super_admin(self):
        url = reverse('adminlogin')
        data = {'email': 'superadmin@example.com', 'password': 'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_custom_super_admin_invalid_credentials(self):
        url = reverse('adminlogin')
        data = {'email': 'superadmin@example.com', 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
