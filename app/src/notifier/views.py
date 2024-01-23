from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def retrieve(self, request, *args, **kwargs):
        # Передаем контекст для включения поля messages
        instance = self.get_object()
        serializer = MailingSerializer(instance, context={'include_messages': True})
        return Response(serializer.data)
