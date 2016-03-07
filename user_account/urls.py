__author__ = 'kolobok'

from django.conf.urls import url, patterns
from django.contrib.auth.views import logout

from user_account.views import authentication, user_agreement, registration, profile

urlpatterns = [
    url(r'^account/login/$', authentication, name='login'),
    url(r'^account/registration/$', registration, name='registration'),
    url(r'^account/logout/$', logout, {'template_name': 'catalog.html'}, name='logout'),
    url(r'^account/profile/$', profile, name='profile'),
    url(r'^account/user_agreement/$', user_agreement, name='user_agreement'),
]
