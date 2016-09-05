from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from user_account.form import AuthenticationForm, RegistrationForm, ProfileChangingEmailForm, \
    ProfileChangingPasswordForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from django import forms


def authentication(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request.POST, auto_id='%s')

        if auth_form.is_valid():
            user_auth = authenticate(username=User.objects.get(email=auth_form.cleaned_data['your_login']),
                                     password=auth_form.cleaned_data['your_password'])

            if user_auth is not None and user_auth.is_active:
                login(request, user_auth)
                return HttpResponseRedirect('/')
            else:
                auth_form.add_error(None, forms.ValidationError(
                    u"Пользователя с такой электронной почтой или паролем не найден"))
    else:
        auth_form = AuthenticationForm(auto_id='%s')

    return render(request, 'login.html', {'auth_form': auth_form, 'reg_form': RegistrationForm(auto_id='%s')})


def registration(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST, auto_id='%s')
        email_username = reg_form.cleaned_data['email_signup']

        if reg_form.is_valid() and checking_email_user(email_username):
            if create_user(email_username, reg_form.cleaned_data['password_signup']):
                user = authenticate(username=email_username,
                                    password=reg_form.cleaned_data['password_signup'])
                if user is not None and user.is_active:
                    login(request, user)
                    send_notice(email_username)
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


class ChangingEmailForm(FormView):
    form_class = ProfileChangingEmailForm
    template_name = 'profile_email.html'

    def get_initial(self):
        initial = super(ChangingEmailForm, self).get_initial()
        initial['email'] = self.request.user.email
        return initial

    def get_context_data(self, **kwargs):
        context = super(ChangingEmailForm, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.save()
        return super(ChangingEmailForm, self).form_valid(form)


class ChangingPasswordForm(FormView):
    form_class = ProfileChangingPasswordForm
    template_name = 'profile_password.html'

    def get_initial(self):
        initial = super(ChangingPasswordForm, self).get_initial()
        initial['password_new'] = self.request.user.email
        print(initial)
        return initial

    def get_context_data(self, **kwargs):
        context = super(ChangingPasswordForm, self).get_context_data(**kwargs)
        context['changing_password_form'] = self.form_class
        return context

    def form_valid(self, form):
        user = self.request.user
        password_new = form.cleaned_data['password_new']
        password_old = form.cleaned_data['password_old']
        if password_new != password_old and user.check_password(password_old):
            user.set_password(password_new)
            user.save()
        return super(ChangingPasswordForm, self).form_valid(form)


def checking_email_user(email):
    return User.objects.filter(email=email).count() == 0


def create_user(email, password):
    user = User.objects.create_user(username=email, email=email, password=password)
    return user.save()


def send_notice(recipient_email):
    file = open('./static/notice.html', 'r')

    subject = u'Регистрация на сайте mycollectioncoin.ru'
    message = file.read()
    from_email = 'qwerty@qwerty.ru'
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list)