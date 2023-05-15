from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser, Money, Message


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password')
        self.admin = CustomUser.objects.create_user(email='admin@example.com', password='password', is_staff=True)
        self.message_data = {'subject': 'Test Subject', 'body': 'Test Body'}

    def test_user_update_view(self):
        url = reverse('user-update')
        self.client.force_authenticate(user=self.user)

        response = self.client.put(url, {'first_name': 'John', 'last_name': 'Doe'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_balance_view_get(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'balance': 0})  # Assuming initial balance is 0

    def test_balance_view_post_add(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, {'amount': '10', 'action': 'add'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        money = Money.objects.get(user=self.user)
        self.assertEqual(money.total, 10)

    def test_balance_view_post_sub(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)
        Money.objects.create(user=self.user, total=20)

        response = self.client.post(url, {'amount': '10', 'action': 'sub'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        money = Money.objects.get(user=self.user)
        self.assertEqual(money.total, 10)

    def test_balance_view_post_invalid_amount(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, {'amount': 'invalid', 'action': 'add'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid amount provided'})

    def test_balance_view_post_invalid_action(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, {'amount': '10', 'action': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action provided. Only "add" or "sub" allowed.'})

    def test_balance_view_post_insufficient_funds(self):
        url = reverse('balance')
        self.client.force_authenticate(user=self.user)
        Money.objects.create(user=self.user, total=10)

        response = self.client.post(url, {'amount': '20', 'action': 'sub'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Insufficient funds'})

    def test_send_message(self):
        url = reverse('send-message')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, self.message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Message.objects.filter(sender=self.user, recipient=self.admin, subject='Test Subject', body='Test Body').exists())
        self.assertEqual(response.json(), {'success': True})

