import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from mailing.models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('message', 'frequency', 'clients', 'date_time', 'end_date_time')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['message'].queryset = Message.objects.all()
        else:
            self.fields['message'].queryset = Message.objects.filter(user=user)
        self.fields['date_time'].widget.attrs['class'] = 'datetimepicker'
        self.fields['end_date_time'].widget.attrs['class'] = 'datetimepicker2'
        self.fields['end_date_time'].required = False
        self.helper = FormHelper(self)

    def clean(self):
        clean_data = super().clean()
        if not clean_data.get('end_date_time'):
            clean_data['end_date_time'] = datetime.datetime(9999, 12, 31, 23, 59)
        return clean_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('user',)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].required = False
