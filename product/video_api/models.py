from django.db import models


class MotionReg(models.Model):
    place_id = models.CharField('ID магазина', max_length=20, default='')
    time_start = models.DateTimeField('Дата\Время события')
    duration = models.IntegerField('Длительность сек.')

    class Meta():
        verbose_name = 'События: движение'
        verbose_name_plural = 'События: движение'

    def __str__(self):
        return '{} : {}'.format(self.place_id)
