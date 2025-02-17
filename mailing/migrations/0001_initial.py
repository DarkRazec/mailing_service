# Generated by Django 5.0.6 on 2024-06-29 19:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=100, unique=True, verbose_name='почта')),
                ('first_name', models.CharField(max_length=50, verbose_name='имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='фамилия')),
                ('middle_name', models.CharField(max_length=50, verbose_name='отчество')),
                ('comment', models.TextField(verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
                'ordering': ('first_name', 'last_name', 'middle_name', 'mail'),
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='дата и время отправки')),
                ('end_date_time', models.DateTimeField(blank=True, null=True, verbose_name='дата и время окончания')),
                ('status', models.CharField(choices=[('запущена', 'успешно'), ('завершена', 'завершена'), ('создана', 'создана')], default='создана', verbose_name='статус')),
                ('frequency', models.CharField(choices=[('однократно', 'однократно'), ('ежедневно', 'ежедневно'), ('еженедельно', 'еженедельно')], default='однократно', verbose_name='периодичность')),
                ('clients', models.ManyToManyField(to='mailing.client', verbose_name='клиенты')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
                'ordering': ('status', 'date_time', 'end_date_time'),
            },
        ),
        migrations.CreateModel(
            name='AttemptLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='дата и время')),
                ('status', models.BooleanField(default=False, verbose_name='статус')),
                ('response', models.CharField(max_length=100, verbose_name='ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='попытка')),
            ],
            options={
                'verbose_name': 'попытка',
                'verbose_name_plural': 'попытки',
                'ordering': ('status', 'date_time', 'response'),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение'),
        ),
    ]
