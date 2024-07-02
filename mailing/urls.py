from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import HomePageView, MailingCreateView, MessageCreateView, MailingDetailView, \
    MailingDeleteView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView, \
    MessageDetailView, MessageUpdateView, MessageDeleteView, ClientListView, MailingListView, MessageListView, \
    AttemptLogsListView, AttemptDetailView, MailingUpdateView, mailing_activity, user_activity

app_name = MailingConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_activity/<int:pk>/', mailing_activity, name='mailing_activity'),
    path('user_activity/<int:pk>/', user_activity, name='user_activity'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('attempts/', AttemptLogsListView.as_view(), name='attempts'),
    path('attempts_detail/<int:pk>/', AttemptDetailView.as_view(), name='attempt_detail'),
]
