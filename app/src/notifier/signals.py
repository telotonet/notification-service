from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Client, Mailing
from .db_queries import get_clients_queryset
from .celery_tasks import send_message
import logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Client)
def update_operator_code(sender, instance, **kwargs):
    logger.info(f"Updating operator code for Client ID {instance.id}")
    # при создании или изменении объекта Client обновляем значение поля operator_code
    instance.operator_code = str(instance.phone_number)[1:4]


@receiver(post_save, sender=Mailing)
def handle_mailing_change(sender, instance, created, **kwargs):
    logger.info(f"Mailing {'created' if created else 'updated'}: ID {instance.id}")
    if created:
        clients = get_clients_queryset(instance)
        for client in clients:
            send_message.apply_async(args=(instance.id, client.id), eta=instance.start_at, expires=instance.end_at)
