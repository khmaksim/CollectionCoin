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
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from collection import settings

from collection.views import main, coins_section, information_coin, add_to_collection, my_collection, catalog

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('user_account.urls', namespace='user_account', app_name='user_account')),
    url(r'^catalog/$', catalog, name='catalog'),
    url(r'^my-collection/$', my_collection, name='my_collection'),
    url(r'^catalog/(?P<id_section>[0-9]+)/$', coins_section, name='coins_section'),
    url(r'^catalog/([0-9]+)/(?P<id_coin>[0-9]+)/$', information_coin, name='information_coin'),
    url(r'^catalog/([0-9]+)/(?P<id_coin>[0-9]+)/add/$', add_to_collection, name='add_to_collection'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

