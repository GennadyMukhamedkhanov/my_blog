from django.db import models


class Like(models.Model):
    photo = models.ForeignKey(to='Photo', on_delete=models.CASCADE, related_name='likes', verbose_name='Фото')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='likes', verbose_name='Имя автора')
    is_like = models.BooleanField()


    def __str__(self):
        return f'{self.photo}   ' \
               f'{self.user}   ' \
               f'{self.is_like}'

    class Meta:
        db_table = 'like'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
