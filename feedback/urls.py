from django.conf.urls import url
from feedback.views import feedback

urlpatterns = [
    url(r'^feedback/$', feedback, name='feedback'),
]
