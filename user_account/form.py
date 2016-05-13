__author__ = 'kolobok'

from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from registration.forms import UserCreationForm
# from django.forms.utils import ErrorList
from django.contrib.auth.models import User


# class SpanErrorList(ErrorList):
#     def __str__(self):              # __unicode__ on Python 2
#         return self.as_span()
#
#     def as_span(self):
#         if not self:
#             return ''
#         return '<span class="errorlist">%s</div>' % '.'.join([e for e in self])


class AuthenticationUserForm(forms.Form):
    your_email = forms.CharField(label=u'Ваш адрес электронной почты', widget=forms.TextInput(
        attrs={'placeholder': 'mymail@mail.com', 'required': 'required'}), max_length=50, required=True,
        error_messages={'required': u'Вы не указали адрес электронной почты',
                        'invalid': u'Адрес электронной почты указан не верно'})
    your_password = forms.CharField(label=u'Ваш пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True,
        error_messages={'required': u'Вы не указали пароль'})
    # keep_me_login = forms.BooleanField(label=u'Оставаться в системе', widget=forms.CheckboxInput(
    #     attrs={'value': 'loginkeeping'}), required=False)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label=u'Адрес электронной почты', widget=forms.EmailInput(
        attrs={'placeholder': 'mymail@mail.com', 'required': 'required'}), max_length=50, required=True,
        error_messages={'unique': u"Пользователь с таким адресом уже существует"})
    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True)
    password2 = None
    # keep_me_login = forms.BooleanField(label=u'Оставаться в системе', widget=forms.CheckboxInput(
    # attrs={'value': 'loginkeeping'}), required=False)

    class Meta(UserCreationForm.Meta):
        fields = [
            'username',
            'password1',
        ]
        exclude = [
            'email',
            'password2',
        ]


class ProfileChangingEmailForm(forms.Form):
    saved = False
    email = forms.EmailField(label=u'Ваш адрес электронной почты', required=True)


class ProfileChangingPasswordForm(forms.Form):
    saved = False
    password_old = forms.CharField(label=u'Старый пароль', widget=forms.PasswordInput(), required=True)
    password_new = forms.CharField(label=u'Новый пароль', widget=forms.PasswordInput(), required=True)
    # password_new_repeat = forms.CharField(label=u'Повторить новый пароль', widget=forms.PasswordInput(), required=True)


class PasswordResetFormInherited(PasswordResetForm):
    email = forms.EmailField(label=u'Адрес элетронной почты указанный при регистрации', required=True,
                             error_messages={'invalid': u'Адрес электронной почты указан не верно'})

    def clean_email(self):
        data = self.cleaned_data['email']
        user = User.objects.filter(email=data)
        if not user.exists():
            raise forms.ValidationError(u"Указанные адрес электронной почты не зарегистрирован")
        return data


class SetPasswordFormInherited(SetPasswordForm):
    new_password1 = forms.CharField(label=u'Новый пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True)
    new_password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True)
