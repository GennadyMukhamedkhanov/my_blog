from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Текст записи')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    status = models.BooleanField(default=False, verbose_name='Статус')
    author = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='photos',verbose_name='Имя автора')
    img = models.ImageField(upload_to='image/%Y', verbose_name='Изображение')

    def __str__(self):
        return f'{self.title}   ' \
               f'{self.description}   ' \
               f'{self.create_at}   ' \
               f'{self.author}   '


    class Meta:
        db_table = 'photo'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'