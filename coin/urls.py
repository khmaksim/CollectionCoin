"""coin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout
from coin import settings

from coin.views import main, coins_section, information_coin
from user_account.views import authentication, user_agreement, registration, profile

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main, name='main'),
    url(r'^account/login/$', authentication, name='login'),
    url(r'^account/registration/$', registration, name='registration'),
    url(r'^account/logout/$', logout, {'template_name': 'index.html'}, name='logout'),
    url(r'^account/profile/$', profile, name='profile'),
    url(r'^account/user_agreement/$', user_agreement, name='user_agreement'),
    url(r'^sections/(?P<id_section>[0-9]+)/$', coins_section, name='coins_section'),
    url(r'^sections/([0-9]+)/coins/(?P<id_coin>[0-9]+)/$', information_coin, name='information_coin'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

