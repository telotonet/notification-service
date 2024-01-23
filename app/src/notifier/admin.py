from django.contrib import admin
from .models import Mailing, Client, Message
import logging
logger = logging.getLogger(__name__)

class MessageInline(admin.TabularInline):
    model = Message
    readonly_fields = ['id', 'dispatch_at', 'status', 'mailing', 'client']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'start_at', 'end_at', 'operator_code', 'client_tag']
    list_display_links = ['id', 'content']
    inlines = [MessageInline]
    def save_model(self, request, obj, form, change):
        logger.info(f"Mailing {'created' if change else 'changed'}: ID {obj.id}")
        super().save_model(request, obj, form, change)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'operator_code', 'timezone', 'tag']
    list_display_links = ['id', 'phone_number']
    readonly_fields = ['operator_code']
    def save_model(self, request, obj, form, change):
        logger.info(f"Сlient {'created' if change else 'changed'}: ID {obj.id}")
        super().save_model(request, obj, form, change)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'dispatch_at', 'status', 'mailing', 'client']
    def save_model(self, request, obj, form, change):
        logger.info(f"Message {'created' if change else 'changed'}: ID {obj.id}")
        super().save_model(request, obj, form, change)