from django.conf.urls import include, url
from django.contrib.auth.views import logout
from user_account.views import authentication, user_agreement, registration, profile, ChangingEmailForm, \
    ChangingPasswordForm

urlpatterns = [
    url(r'^account/login/$', authentication, name='login'),
    url(r'^account/registration/$', registration, name='registration'),
    url(r'^account/logout/$', logout, {'template_name': 'catalog.html'}, name='logout'),
    url(r'^account/profile/$', profile, name='profile'),
    url(r'^account/profile/contacts/$', ChangingEmailForm.as_view(), name='contacts'),
    url(r'^account/profile/security/$', ChangingPasswordForm.as_view(), name='security'),
    url(r'^account/user_agreement/$', user_agreement, name='user_agreement'),
    url(r'^account/', include('registration.backends.hmac.urls')),
]
