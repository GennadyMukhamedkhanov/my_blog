from django.db import models


class Comment(models.Model):
    text = models.TextField(blank=True, verbose_name='Комментарий')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ForeignKey(to='Photo', on_delete=models.CASCADE, related_name='comments', verbose_name='Фото')
    user = models.ForeignKey(to='User', verbose_name='Имя автора', related_name='comments', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.photo}   ' \
               f'{self.text}   ' \
               f'{self.user}'

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
