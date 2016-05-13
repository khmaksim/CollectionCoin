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
from collection import settings
from collection.views import main, section_catalog, section_collection, \
    information_coin, add_to_collection, my_collection, catalog, remove_from_collection, coin_collection

urlpatterns = [
    url(r'^$', main),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('user_account.urls', namespace='user_account', app_name='user_account')),
    url(r'^collection/$', my_collection, name='collection'),
    url(r'^collection/(?P<id_section>[0-9]+)/$', section_collection, name='section_collection'),
    url(r'^collection/([0-9]+)/([0-9]+)/(?P<id_collection>[0-9]+)$', coin_collection, name='coin_collection'),
    url(r'^collection/([0-9]+)/(?P<id_coin>[0-9]+)/remove/$', remove_from_collection, name='remove_from_collection'),
    url(r'^catalog/$', catalog, name='catalog'),
    url(r'^catalog/(?P<id_section>[0-9]+)/$', section_catalog, name='section_catalog'),
    url(r'^catalog/([0-9]+)/(?P<id_coin>[0-9]+)/$', information_coin, name='information_coin'),
    url(r'^catalog/([0-9]+)/(?P<id_coin>[0-9]+)/add/$', add_to_collection, name='add_to_collection'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

