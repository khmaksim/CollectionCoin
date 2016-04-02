__author__ = 'kolobok'

from django.forms import ModelForm
from django.forms.widgets import TextInput, SelectMultiple, Select
from collection.models import Coin, Collection


class CoinForm(ModelForm):
    class Meta:
        model = Coin
        exclude = ['name', 'year', 'section']
        widgets = {'circulation': TextInput(),
                   'inscription': TextInput(),
                   'weight': TextInput(),
                   'diameter': TextInput(),
                   'thickness': TextInput(),
                   'metal': TextInput(),
                   'type_edge': TextInput(),
                   'mint': Select(), }


class AddToCollectionForm(ModelForm):
    class Meta:
        model = Collection
        exclude = ['coin', 'user']


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        exclude = ['coin', 'user']