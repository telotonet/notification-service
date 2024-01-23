from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from notifier.models import Client


class ClientAPITests(APITestCase):
    def setUp(self):
        self.client_data = {
            'phone_number': '79123456789',
            'operator_code': '912',
            'tag': 'client_tag',
            'timezone': 'Europe/Moscow',
        }

    def test_create_client(self):
        url = reverse('client-list')
        response = self.client.post(url, self.client_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client = Client.objects.last()
        self.assertEqual(client.phone_number, self.client_data['phone_number'])
        self.assertEqual(client.operator_code, self.client_data['phone_number'][1:4])
        self.assertEqual(client.tag, self.client_data['tag'])
        self.assertEqual(client.timezone, self.client_data['timezone'])

    def test_update_client(self):
        client = Client.objects.create(**self.client_data)
        updated_data = {
            'phone_number': '79034440114',
            'operator_code': '903',
            'tag': 'new_tag',
            'timezone': 'America/New_York',
        }
        url = reverse('client-detail', args=[str(client.id)])
        response = self.client.put(url, updated_data, format='json')

        client.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(client.phone_number, updated_data['phone_number'])
        self.assertEqual(client.operator_code, updated_data['operator_code'])
        self.assertEqual(client.tag, updated_data['tag'])
        self.assertEqual(client.timezone, updated_data['timezone'])

    def test_update_client_by_patch(self):
        client = Client.objects.create(**self.client_data)
        updated_data = {'phone_number': '79034440114'}
        url = reverse('client-detail', args=[str(client.id)])
        response = self.client.patch(url, data=updated_data, format='json')
        client.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(client.phone_number, '79034440114')
        self.assertEqual(client.operator_code, '903')
        self.assertEqual(client.tag, self.client_data['tag'])
        self.assertEqual(client.timezone, self.client_data['timezone'])

    def test_delete_client(self):
        client = Client.objects.create(**self.client_data)
        response = self.client.delete(reverse('client-detail', args=[client.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)

    def test_client_list(self):
        Client.objects.create(**self.client_data)
        response = self.client.get(reverse('client-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_client(self):
        client = Client.objects.create(**self.client_data)
        response = self.client.get(reverse('client-detail', args=[client.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
