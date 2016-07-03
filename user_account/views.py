__author__ = 'kolobok'

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, views
from django.views.generic.edit import FormView
from user_account.form import AuthenticationUserForm as AuthForm, RegistrationForm, ChangingEmailForm, \
    ChangingPasswordForm, PasswordResetFormInherited, SetPasswordFormInherited
from django.contrib.auth.models import User
from registration.backends.hmac.views import RegistrationView


def login_registration(request):
    return render(request, 'registration/registration_form.html', {'login_form': AuthForm(auto_id='%s'),
                                                                   'form': RegistrationForm(auto_id='%s')})


def authentication(request):
    auth_form = AuthForm(request.POST or None, auto_id='%s')

    if auth_form.is_valid():
        login_user = User.objects.get(email=auth_form.cleaned_data['your_email'])
        if login_user:
            user = authenticate(username=login_user.username,
                                password=auth_form.cleaned_data['your_password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

        auth_form.add_error(None, u'Адрес электронной почты или пароль указан не верно')

    return render(request, 'registration/registration_form.html', {'login_form': auth_form,
                                                                   'form': RegistrationForm(auto_id='%s')})


# def registration(request):
    # if request.method == 'POST':
    #     reg_form = RegistrationForm(request.POST, auto_id='%s')
    #     email_username = reg_form.cleaned_data['email_signup']
    #
    #     if reg_form.is_valid() and checking_email_user(email_username):
    #         if create_user(email_username, reg_form.cleaned_data['password_signup']):
    #             user = authenticate(username=email_username,
    #                                 password=reg_form.cleaned_data['password_signup'])
    #             if user is not None and user.is_active:
    #                 login(request, user)
    #                 send_notice(email_username)
    #                 return HttpResponseRedirect('/')
    # else:
    #     reg_form = RegistrationForm(auto_id='%s')
    #
    # return render(request, 'registration/registration_form.html', {'auth_form': AuthenticationForm(auto_id='%s'), 'reg_form': reg_form})


def user_agreement(request):
    return render(request, 'user_agreement.html')


# @login_required
class ChangingEmailView(FormView):
    template_name = 'changing_email_form.html'
    form_class = ChangingEmailForm
    success_url = '.'

    def get_initial(self):
        initial = super(ChangingEmailView, self).get_initial()
        initial['email'] = self.request.user.email
        return initial


    def form_valid(self, form):
        user = self.request.user

        user.email = form.cleaned_data['email']
        user.save()
        return super(ChangingEmailView, self).form_valid(form)


# @login_required
class ChangingPasswordView(FormView):
    form_class = ChangingPasswordForm
    template_name = 'changing_password_form.html'
    success_url = '.'

    def form_valid(self, form):
        user = self.request.user

        password_new = form.cleaned_data['password_new']
        password_old = form.cleaned_data['password_old']
        if password_new != password_old and user.check_password(password_old):
            user.set_password(password_new)
            user.save()
            return super(ChangingPasswordView, self).form_valid(form)
        else:
            return super(ChangingPasswordView, self).form_invalid(form)


# def profile(request):
#     user = request.user
#
#     if request.method == 'POST':
#         changing_email_form = ProfileChangingEmailForm(request.POST, initial={'email': user.email})
#
#         if changing_email_form.has_changed():
#             if changing_email_form.is_bound and changing_email_form.is_valid():
#                 user.email = changing_email_form.cleaned_data['email']
#                 user.save()
#                 changing_email_form.saved = True
#
#         changing_password_form = ProfileChangingPasswordForm(request.POST,
#                                                              initial={'password_old': user.password,
#                                                                       'password_new': ''})
#         if changing_password_form.has_changed():
#             if changing_password_form.is_bound and changing_password_form.is_valid():
#                 password_new = changing_password_form.cleaned_data['password_new']
#                 password_old = changing_password_form.cleaned_data['password_old']
#                 if password_new != password_old and user.check_password(password_old):
#                     user.set_password(password_new)
#                     user.save()
#                     changing_password_form.saved = True
#
#     else:
#         changing_email_form = ProfileChangingEmailForm({'email': user.email})
#         changing_password_form = ProfileChangingPasswordForm()
#
#     return render(request, 'profile.html', {'changing_password_form': changing_password_form,
#                                             'changing_email_form': changing_email_form})


# def create_user(email, password):
#     user = User.objects.create_user(username=email, email=email, password=password)
#     return user.save()


class RegisterView(RegistrationView):
    def create_inactive_user(self, form):
        new_user = form.save(commit=False)
        new_user.email = form.cleaned_data['username']
        new_user.is_active = False
        new_user.save()

        # user authorization and login
        if new_user is not None:
            auth_user = authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
            if auth_user is not None:
                login(self.request, auth_user)

        # send notice
        self.send_activation_email(new_user)
        return new_user

    def get_success_url(self, user):
        return 'user_account:registration_complete'


@csrf_protect
def password_reset(request):
    template_response = views.password_reset(request,
                                             template_name='password_reset_form.html',
                                             email_template_name='password_reset_email.html',
                                             subject_template_name='password_reset_subject.txt',
                                             password_reset_form=PasswordResetFormInherited,
                                             post_reset_redirect=reverse('user_account:password_reset_done'))
    return template_response


@csrf_protect
def password_reset_done(request):
    template_response = views.password_reset_done(request, template_name='password_reset_done.html')
    return template_response


@csrf_protect
def password_reset_confirm(request, uidb64, token):
    template_response = views.password_reset_confirm(request,
                                                     template_name='password_reset_confirm.html',
                                                     post_reset_redirect=reverse('user_account:password_reset_complete'),
                                                     set_password_form=SetPasswordFormInherited,
                                                     uidb64=uidb64,
                                                     token=token)

    return template_response


@csrf_protect
def password_reset_complete(request):
    template_response = views.password_reset_complete(request,
                                                      template_name='password_reset_complete.html')
    return template_response
