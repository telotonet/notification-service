from rest_framework import serializers
from django.utils import timezone
from .models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # noqa A003

    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'operator_code', 'tag', 'timezone']


class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = ['dispatch_at', 'status', 'mailing', 'client']


class MailingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # noqa A003
    sent_messages_count = serializers.SerializerMethodField(read_only=True)
    unsent_messages_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mailing
        fields = [
            'id',
            'content',
            'start_at',
            'end_at',
            'operator_code',
            'client_tag',
            'sent_messages_count',
            'unsent_messages_count',
        ]

    def get_sent_messages_count(self, obj):
        return int(obj.messages.filter(status=True).count())

    def get_unsent_messages_count(self, obj):
        return int(obj.messages.filter(status=False).count())

    def to_representation(self, instance):
        if self.context.get('include_messages', False):
            self.fields['messages'] = MessageSerializer(many=True, read_only=True)
        return super().to_representation(instance)

    def validate(self, data):
        start_at = data.get('start_at')
        end_at = data.get('end_at')

        if start_at is not None and end_at is not None:
            if start_at >= end_at:
                raise serializers.ValidationError('Время начала рассылки должно быть позже её окончания.')

        if end_at is not None and end_at <= timezone.now():
            raise serializers.ValidationError('Время окончания рассылки уже прошло.')

        return super().validate(data)
