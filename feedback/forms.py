from django.forms import ModelForm
from feedback.models import *


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['datetime', 'user']
