from django.conf.urls import url
from .views import Messsage

urlpatterns = [
    url(r'^feedback/$', Messsage.as_view(), name='feedback_message'),
]
