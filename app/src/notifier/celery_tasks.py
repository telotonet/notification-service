import requests
from django.shortcuts import get_object_or_404
from django.utils import timezone
from environs import Env
from celery_app import app
from .models import Mailing, Client, Message


env = Env()
env.read_env()


@app.task(bind=True, retry_backoff=True)
def send_message(self, mailing_id, client_id):
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
