# Generated by Django 5.0.6 on 2024-06-30 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_mailing_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ('status', 'date_time', 'end_date_time'), 'permissions': [('set_active', 'Can change is_active field')], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
    ]
