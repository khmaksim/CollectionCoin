__author__ = 'kolobok'

from django.conf.urls import include, url
from django.contrib.auth.views import logout
from user_account.views import authentication, user_agreement, ChangingPasswordView, ChangingEmailView, \
    login_registration, RegisterView, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from user_account.form import RegistrationForm

urlpatterns = [
    url(r'^account/password_reset/$', password_reset, name='password_reset'),
    url(r'^account/password_reset_done/$', password_reset_done, name='password_reset_done'),
    url(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^account/reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^account/$', login_registration, name='login_registration'),
    url(r'^account/login/$', authentication, name='login'),
    url(r'^account/logout/$', logout, {'template_name': 'catalog.html'}, name='logout'),
    url(r'^account/profile/$', ChangingPasswordView.as_view(), name='profile'),
    url(r'^account/profile/changing-password/$', ChangingPasswordView.as_view(), name='changing_password'),
    url(r'^account/profile/changing-email/$', ChangingEmailView.as_view(), name='changing_email'),
    url(r'^account/user_agreement/$', user_agreement, name='user_agreement'),
    url(r'^account/register/$', RegisterView.as_view(form_class=RegistrationForm),
        name='registration_register'),
    url(r'^account/register/#(\S+)$', RegisterView.as_view(form_class=RegistrationForm),
        name='registration_register'),
    url(r'^account/', include('registration.backends.hmac.urls')),
]
