import secrets

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, PasswordRecoveryForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification_send')
    extra_context = {
        'title': 'Регистрация',
    }

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.token = secrets.token_urlsafe(16)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для завершения процесса регистрации перейдите по ссылке {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.groups.add(Group.objects.get(name='users'))
    user.save()
    return redirect(reverse('users:login'))


class VerificationView(TemplateView):
    template_name = 'users/verification_send.html'


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('mailing:homepage')
    extra_context = {
        'title': 'Профиль',
    }

    def get_object(self, queryset=None):
        return self.request.user


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = PasswordRecoveryForm
    template_name = 'users/password_recovery.html'
    extra_context = {'title': 'Восстановление пароля'}

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        password = secrets.token_hex(8)
        user.set_password(password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Здравствуйте, вы запрашивали обновление пароля. Ваш новый пароль: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return render(request, 'users/reset_send.html')
