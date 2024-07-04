from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from blog.models import Post
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Mailing, Message, Client, AttemptLogs
from mailing.services import clear_cache, count_unique_clients


def mailing_activity(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = False if mailing.is_active else True
    mailing.save()
    return redirect(reverse_lazy('mailing:mailing_detail', args=[mailing.pk]))


def user_activity(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.user.is_active = False if mailing.user.is_active else True
    mailing.user.save()
    return redirect(reverse_lazy('mailing:mailing_detail', args=[mailing.pk]))


# HOMEPAGE VIEW
class HomePageView(TemplateView):
    template_name = 'mailing/homepage.html'
    extra_context = {
        'title': 'Главная',
        'timeout': settings.CACHE_TIMEOUT
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if settings.CACHE_ENABLED:
            key = 'counts'
            counts = cache.get(key)
            if counts is None:
                counts = (
                    Mailing.objects.count(),
                    Mailing.objects.filter(is_active=True, status__in=[Mailing.STARTED]).count(),
                    Post.objects.order_by('?')[:3],
                    count_unique_clients()
                )
                cache.set(key, counts, timeout=60)
            context['mailing_count'] = counts[0]
            context['active_mailing_count'] = counts[1]
            context['blog_posts'] = counts[2]
            context['unique_clients'] = counts[3]

        else:
            context['mailing_count'] = Mailing.objects.count()
            context['active_mailing_count'] = (Mailing.objects.filter(is_active=True, status__in=[Mailing.STARTED])
                                               .count())
            context['blog_posts'] = Post.objects.order_by('?')[:3]
            context['unique_clients'] = count_unique_clients()

        return context


# LIST VIEWS
class MailingListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/mailing_list.html'
    model = Mailing
    fields = ('message', 'date_time', 'status',)
    extra_context = {
        'title': 'Рассылки',
        'timeout': settings.CACHE_TIMEOUT
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/message_list.html'
    model = Message
    fields = '__all__'
    extra_context = {
        'title': 'Письма',
        'timeout': settings.CACHE_TIMEOUT
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/client_list.html'
    model = Client
    fields = '__all__'
    extra_context = {
        'title': 'Клиенты',
        'timeout': settings.CACHE_TIMEOUT
    }


class AttemptLogsListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/attempt_list.html'
    model = AttemptLogs
    fields = ('mailing', 'status',)
    extra_context = {
        'title': 'Логи',
        'timeout': settings.CACHE_TIMEOUT
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return AttemptLogs.objects.all()
        return AttemptLogs.objects.filter(mailing__user=self.request.user)


# CREATE VIEWS
class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    template_name = 'mailing/create.html'
    form_class = MailingForm
    permission_required = 'mailing.add_mailing'
    extra_context = {
        'title': 'Создание рассылки',
        'viewname': 'mailing:mailing_detail'
    }
    success_url = reverse_lazy('mailing:homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            return super().form_valid(form)
        return super().form_invalid(form)


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    template_name = 'mailing/create.html'
    form_class = MessageForm
    permission_required = 'mailing.add_message'
    extra_context = {
        'title': 'Создание письма',
        'viewname': 'mailing:message_detail'
    }
    success_url = reverse_lazy('mailing:homepage')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            return super().form_valid(form)
        return super().form_invalid(form)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    template_name = 'mailing/create.html'
    form_class = ClientForm
    permission_required = 'mailing.add_client'
    extra_context = {
        'title': 'Создание пользователя',
        'viewname': 'mailing:client_detail'
    }
    success_url = reverse_lazy('mailing:homepage')


# DETAIL VIEWS
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    success_url = reverse_lazy('mailing:mailing_detail')
    extra_context = {'timeout': settings.CACHE_TIMEOUT}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Рассылка: {self.get_object()}'
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    success_url = reverse_lazy('mailing:message_detail')
    extra_context = {'timeout': settings.CACHE_TIMEOUT}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Письмо: {self.object.title}'
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    success_url = reverse_lazy('mailing:client_detail')
    extra_context = {'timeout': settings.CACHE_TIMEOUT}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Клиент: {self.object.mail}'
        return context


class AttemptDetailView(LoginRequiredMixin, DetailView):
    model = AttemptLogs
    template_name = 'mailing/attempt_detail.html'
    success_url = reverse_lazy('mailing:attempt_detail')
    extra_context = {'timeout': settings.CACHE_TIMEOUT}


# UPDATE VIEWS
class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    template_name = 'mailing/create.html'
    form_class = MailingForm
    permission_required = 'mailing.update_mailing'
    extra_context = {
        'title': 'Редактирование рассылки',
        'viewname': 'mailing:mailing_detail'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', args=[self.kwargs.get('pk')])


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    template_name = 'mailing/create.html'
    form_class = MessageForm
    permission_required = 'mailing.update_message'
    extra_context = {
        'title': 'Редактирование письма',
        'viewname': 'mailing:message_detail'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', args=[self.kwargs.get('pk')])


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    template_name = 'mailing/create.html'
    form_class = ClientForm
    permission_required = 'mailing.update_client'
    extra_context = {
        'title': 'Редактирование данных пользователя',
        'viewname': 'mailing:client_detail'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', args=[self.kwargs.get('pk')])


# DELETE VIEWS
class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy("mailing:homepage")

    def form_valid(self, form):
        clear_cache('mailing', {self.object.id})
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy("mailing:homepage")

    def form_valid(self, form):
        clear_cache('message', {self.object.id})
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy("mailing:homepage")

    def form_valid(self, form):
        clear_cache('client', {self.object.id})
        return super().form_valid(form)
