from django.db import models

class Data(models.Model):
    pubtime = models.DateField(verbose_name='日期')
    mood = models.FloatField(verbose_name='心情')
    mood_keywords = models.CharField(max_length=255, default='', verbose_name='心情关键词')
    consume = models.FloatField(default=0.0, verbose_name='消费额(元)')
    consume_keywords = models.CharField(max_length=255, default='', verbose_name='消费关键词')
    time_keywords = models.CharField(max_length=255, default='', verbose_name='时间分布(时)')

    consume_log = models.TextField(default='', verbose_name='消费日志')
    time_log = models.TextField(default='', verbose_name='时间日志')
    event_log = models.TextField(default='', verbose_name='事件日志')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '数据'

    def __str__(self):
        return str(self.pubtime)
