from django.contrib import admin

from mailing.models import Mailing, Client, Message, AttemptLogs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'status', )
    search_fields = ('user',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('email',)


@admin.register(AttemptLogs)
class AttemptLogsAdmin(admin.ModelAdmin):
    list_display = ('mailing',)
