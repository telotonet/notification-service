import datetime
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from notifier.models import Mailing
from notifier.factories import MailingFactory, MessageFactory, ClientFactory


class MailingViewSetTests(APITestCase):

    def setUp(self):
        self.mailing = MailingFactory()
        self.mailing_recipient = ClientFactory()
        self.message = MessageFactory(mailing=self.mailing, client=self.mailing_recipient)

    def test_list_mailing(self):
        Mailing.objects.all().delete()
        MailingFactory.create_batch(10)
        response = self.client.get(reverse('mailing-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_create_mailing(self):
        Mailing.objects.all().delete()
        url = reverse('mailing-list')
        mailing_data = {
            'content': 'Mailing text',
            'start_at': timezone.now().isoformat(),
            'end_at': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'operator_code': '123',
            'client_tag': 'example_tag',
        }

        response = self.client.post(url, mailing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_mailing = Mailing.objects.last()
        self.assertEqual(Mailing.objects.count(), 1)
        self.assertEqual(created_mailing.content, mailing_data['content'])
        self.assertEqual(created_mailing.start_at.isoformat(), mailing_data['start_at'])
        self.assertEqual(created_mailing.end_at.isoformat(), mailing_data['end_at'])
        self.assertEqual(created_mailing.operator_code, mailing_data['operator_code'])
        self.assertEqual(created_mailing.client_tag, mailing_data['client_tag'])

    def test_retrieve_mailing(self):
        url = reverse('mailing-detail', args=[self.mailing.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.mailing.content, response.data['content'])
        self.assertEqual(self.mailing.operator_code, int(response.data['operator_code']))
        self.assertEqual(self.mailing.start_at, datetime.datetime.fromisoformat(response.data['start_at']))
        self.assertEqual(self.mailing.end_at, datetime.datetime.fromisoformat(response.data['end_at']))
        self.assertEqual(self.mailing.operator_code, int(response.data['operator_code']))

    def test_update_mailing(self):
        new_mailing = {
            'content': 'Mailing text',
            'start_at': timezone.now().isoformat(),
            'end_at': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'operator_code': '123',
            'client_tag': 'example_tag',
        }
        url = reverse('mailing-detail', args=[str(self.mailing.id)])
        response = self.client.put(url, new_mailing, format='json')

        self.mailing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.mailing.content, new_mailing['content'])
        self.assertEqual(self.mailing.start_at.isoformat(), new_mailing['start_at'])
        self.assertEqual(self.mailing.end_at.isoformat(), new_mailing['end_at'])
        self.assertEqual(self.mailing.operator_code, new_mailing['operator_code'])
        self.assertEqual(self.mailing.client_tag, new_mailing['client_tag'])

    def test_update_mailing_by_patch(self):
        updated_data = {'content': 'Updated message content'}
        url = reverse('mailing-detail', args=[str(self.mailing.id)])

        response = self.client.patch(url, data=updated_data, format='json')
        self.mailing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.mailing.content, 'Updated message content')

    def test_delete_mailing(self):
        url = reverse('mailing-detail', args=[str(self.mailing.id)])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mailing.objects.count(), 0)
