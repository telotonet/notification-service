import requests
from django.shortcuts import get_object_or_404
from django.utils import timezone
from environs import Env
from celery_app import app
from .models import Mailing, Client, Message
import pytz

import logging
logger = logging.getLogger(__name__)


env = Env()
env.read_env()


@app.task(bind=True, retry_backoff=True)
def send_message(self, mailing_id, client_id):
    try:
        mailing = get_object_or_404(Mailing, id=mailing_id)
        client = get_object_or_404(Client, id=client_id)

        token = env('API_TOKEN')
        url = 'https://probe.fbrq.cloud/v1/send/'
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        message = Message.objects.create(mailing=mailing, client=client)
        payload = {'id': message.id, 'phone': client.phone_number, 'text': mailing.content}
        try:
            response = requests.post(url=url + str(message.id), headers=header, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise self.retry(exc=exc)
        else:
            now = timezone.now()
            message.dispatch_at = now
            message.status = True
            message.save()

        client_tz = pytz.timezone(client.timezone)
        current_client_time = timezone.now().astimezone(client_tz).time()
        if mailing.time_interval_start and mailing.time_interval_end:
            if not (mailing.time_interval_start <= current_client_time <= mailing.time_interval_end):
                return  # Пропускаем отправку, если время не подходит

        logger.info(f"Message sent: Mailing ID {mailing_id}, Client ID {client_id}")

    except requests.exceptions.RequestException as exc:
        logger.error(f"Error sending message: {exc}")
        raise self.retry(exc=exc)
