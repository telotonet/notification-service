from .models import Client


def get_clients_queryset(mailing):
    filters = {}

    if mailing.operator_code:
        filters['operator_code'] = mailing.operator_code

    if mailing.client_tag:
        filters['tag'] = mailing.client_tag

    return Client.objects.filter(**filters)
