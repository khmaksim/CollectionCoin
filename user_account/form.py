from django import forms
from django.contrib.auth.models import User


class AuthenticationForm(forms.Form):
    your_login = forms.CharField(label=u'Ваш email', widget=forms.TextInput(
        attrs={'placeholder': 'mymail@mail.com', 'required': 'required'}), max_length=50, required=True)
    your_password = forms.CharField(label=u'Ваш пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True)
    # keep_me_login = forms.BooleanField(label=u'Оставаться в системе', widget=forms.CheckboxInput(
    #     attrs={'value': 'loginkeeping'}), required=False)

    # user validation by email
    def clean(self):
        cleaned_data = super(AuthenticationForm, self).clean()
        try:
            User.objects.get(email=cleaned_data.get('your_login'))
        except User.DoesNotExist:
            raise forms.ValidationError(u"Пользователя с такой электронной почтой или паролем не найден")
        return cleaned_data


class RegistrationForm(forms.Form):
    email_signup = forms.CharField(label=u'Ваш email', widget=forms.EmailInput(
        attrs={'placeholder': 'mymail@mail.com', 'required': 'required'}), max_length=50, required=True)
    password_signup = forms.CharField(label=u'Ваш пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'abc123DEF .!', 'required': 'required'}), max_length=50, required=True)

    # keep_me_login = forms.BooleanField(label=u'Оставаться в системе', widget=forms.CheckboxInput(
    # attrs={'value': 'loginkeeping'}), required=False)


class ProfileChangingEmailForm(forms.Form):
    saved = False
    email = forms.EmailField(label=u'Ваш email', required=True)


class ProfileChangingPasswordForm(forms.Form):
    saved = False
    password_old = forms.CharField(label=u'Старый пароль', widget=forms.PasswordInput(), required=True)
    password_new = forms.CharField(label=u'Новый пароль', widget=forms.PasswordInput(), required=True)
    # password_new_repeat = forms.CharField(label=u'Повторить новый пароль', widget=forms.PasswordInput(), required=True)
