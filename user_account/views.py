__author__ = 'kolobok'

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from user_account.form import AuthenticationForm, RegistrationForm, ProfileChangingEmailForm, ProfileChangingPasswordForm
from django.contrib.auth.models import User


def authentication(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request.POST, auto_id='%s')

        if auth_form.is_valid():
            user = authenticate(username=auth_form.cleaned_data['your_login'],
                                password=auth_form.cleaned_data['your_password'])
            if user is not None and user.is_active:
                login(request, user)
                print(request.user.is_authenticated())
                return HttpResponseRedirect('/')
    else:
        auth_form = AuthenticationForm(auto_id='%s')

    return render(request, 'login.html', {'auth_form': auth_form, 'reg_form': RegistrationForm(auto_id='%s')})


def registration(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST, auto_id='%s')

        if reg_form.is_valid():
            if create_user(reg_form.cleaned_data['email_signup'], reg_form.cleaned_data['password_signup']):
                user = authenticate(username=reg_form.cleaned_data['email_signup'],
                                    password=reg_form.cleaned_data['password_signup'])
                if user is not None and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        reg_form = RegistrationForm(auto_id='%s')

    return render(request, 'login.html', {'auth_form': AuthenticationForm(auto_id='%s'), 'reg_form': reg_form})


def user_agreement(request):
    return render(request, 'user_agreement.html')


def profile(request):
    user = request.user

    if request.method == 'POST':
        changing_email_form = ProfileChangingEmailForm(request.POST, initial={'email': user.email})
        if changing_email_form.has_changed():
            if changing_email_form.is_bound and changing_email_form.is_valid():
                user.email = changing_email_form.cleaned_data['email']
                user.save()
                changing_email_form.saved = True

        changing_password_form = ProfileChangingPasswordForm(request.POST,
                                                             initial={'password_old': user.password,
                                                                      'password_new': ''})
        if changing_password_form.has_changed():
            if changing_password_form.is_bound and changing_password_form.is_valid():
                password_new = changing_password_form.cleaned_data['password_new']
                password_old = changing_password_form.cleaned_data['password_old']
                if password_new != password_old and user.check_password(password_old):
                    user.set_password(password_new)
                    user.save()
                    changing_password_form.saved = True

    else:
        changing_email_form = ProfileChangingEmailForm({'email': user.email})
        changing_password_form = ProfileChangingPasswordForm()

    return render(request, 'profile.html', {'changing_password_form': changing_password_form,
                                            'changing_email_form': changing_email_form})


def create_user(email, password):
    user = User.objects.create_user(username=email, email=email, password=password)
    return user.save()