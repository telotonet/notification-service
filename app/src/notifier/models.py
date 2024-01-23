import zoneinfo
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import logging
logger = logging.getLogger(__name__)

class Mailing(models.Model):
    content = models.TextField('Сообщение')
    start_at = models.DateTimeField('Время запуска')
    end_at = models.DateTimeField('Время окончания')
    operator_code = models.CharField('Код оператора клиента', max_length=3, blank=True)
    client_tag = models.CharField('Тег клиента', max_length=50, blank=True)
    time_interval_start = models.TimeField('Начало временного интервала', null=True, blank=True)
    time_interval_end = models.TimeField('Конец временного интервала', null=True, blank=True)


    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка с id: {self.id}'

    def clean(self):
        if self.end_at <= self.start_at:
            logger.error(f"Mailing validation error: ID {self.id}")
            raise ValidationError(
                'Время начала рассылки должно быть позже её окончания.',
            )


class Client(models.Model):
    TIMEZONE_CHOICES = ((x, x) for x in sorted(zoneinfo.available_timezones(), key=str.lower))
    phone_number = models.CharField(
        'Номер телефона',
        unique=True,
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^7\d{10}$',
                message='Номер должен состоять из 11 цифр и начинаться с 7',
            ),
        ],
    )
    operator_code = models.CharField('Код оператора', max_length=3, blank=True)
    tag = models.CharField('Тег', max_length=50, db_index=True)
    timezone = models.CharField(
        'Часовой пояс',
        choices=TIMEZONE_CHOICES,
        max_length=250,
        default='Europe/Moscow',
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return str(self.phone_number)


class Message(models.Model):
    dispatch_at = models.DateTimeField('Время отправки', null=True, blank=True)
    status = models.BooleanField('Статус', default=False)
    mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
