from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    email = models.EmailField(u'Ваш email для связи')
    name_sender = models.CharField(u'Ваше имя', max_length=20)
    message = models.TextField(u'Ваше сообщение')
    datetime = models.DateTimeField(u'Дата и время отправки')
    user = models.ForeignKey(User, verbose_name=u'Пользователь', db_column='id_user')

    def __str__(self):
        return "%s - %s" % (self.sender, self.text)

    class Meta:
        verbose_name = u'Обратная связь'
        verbose_name_plural = u'Обратная связь'
