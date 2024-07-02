from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    mail = models.EmailField(max_length=100, unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='отчество')
    comment = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return f'{self.mail}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('first_name', 'last_name', 'middle_name', 'mail',)


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        ordering = ('title',)


class Mailing(models.Model):
    STARTED = 'запущена'
    COMPLETED = 'завершена'
    NEW = 'создана'
    STATUS_TYPE = (
        (STARTED, 'успешно'),
        (COMPLETED, 'завершена'),
        (NEW, 'создана'),
    )

    ONCE = 'однократно'
    DAILY = 'ежедневно'
    WEEKLY = 'еженедельно'
    FREQUENCY = (
        (ONCE, 'однократно'),
        (DAILY, 'ежедневно'),
        (WEEKLY, 'еженедельно'),
    )

    date_time = models.DateTimeField(verbose_name='дата и время отправки')
    end_date_time = models.DateTimeField(verbose_name='дата и время окончания', **NULLABLE)
    status = models.CharField(choices=STATUS_TYPE, default=NEW, verbose_name='статус')
    frequency = models.CharField(choices=FREQUENCY, default=ONCE, verbose_name='периодичность')
    is_active = models.BooleanField(default=True, verbose_name='активность')
    message = models.OneToOneField(Message, verbose_name='сообщение', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('status', 'date_time', 'end_date_time')

        permissions = [
            (
                'set_active',
                'Can change is_active field'
            ),
        ]


class AttemptLogs(models.Model):
    date_time = models.DateTimeField(verbose_name='дата и время')
    status = models.BooleanField(default=False, verbose_name='статус')
    response = models.CharField(max_length=100, verbose_name='ответ сервера')
    mailing = models.ForeignKey(Mailing, verbose_name='попытка', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
        ordering = ('status', 'date_time', 'response',)
