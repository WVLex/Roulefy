from django.db import models


class Users(models.Model):
    room_id = models.CharField('ID комнаты', max_length=4)
    user_name = models.CharField('Имя пользователя', max_length=250)
    song_list = models.TextField('Список песен')
    date = models.DateTimeField('Дата и время')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
