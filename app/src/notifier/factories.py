import zoneinfo
from datetime import timedelta
from django.utils import timezone
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from notifier.models import Mailing, Message, Client


class MailingFactory(DjangoModelFactory):
    class Meta:
        model = Mailing

    content = Faker('text')
    start_at = Faker('date_time_this_year', after_now=True, before_now=False)
    end_at = Faker('date_time_this_year', after_now=True, before_now=False)
    operator_code = Faker('random_number', digits=3)
    client_tag = Faker('word')

    @classmethod
    def create(cls, **kwargs):
        # Ensure end_at is greater than start_at
        start_at = kwargs.get('start_at', timezone.now())
        end_at = kwargs.get('end_at', start_at + timedelta(days=1))
        if end_at <= start_at:
            end_at = start_at + timedelta(days=1)

        return super().create(start_at=start_at, end_at=end_at, **kwargs)


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    phone_number = Faker('pyint', min_value=70000000000, max_value=79999999999)

    operator_code = Faker('random_number', digits=3)
    tag = Faker('word')
    timezone = Faker(
        'random_element',
        elements=[(x, x) for x in sorted(zoneinfo.available_timezones(), key=str.lower)],
    )


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    dispatch_at = Faker('date_time_this_year', after_now=True, before_now=False)
    status = Faker('boolean')
    mailing = SubFactory(MailingFactory)
    client = SubFactory(ClientFactory)
