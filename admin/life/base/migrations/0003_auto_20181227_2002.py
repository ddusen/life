# Generated by Django 2.1.4 on 2018-12-27 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_data_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='keywords',
        ),
        migrations.AddField(
            model_name='data',
            name='consume_keywords',
            field=models.CharField(default='', max_length=255, verbose_name='消费关键词'),
        ),
        migrations.AddField(
            model_name='data',
            name='monetary',
            field=models.FloatField(default=0.0, verbose_name='消费额'),
        ),
        migrations.AddField(
            model_name='data',
            name='mood_keywords',
            field=models.CharField(default='', max_length=255, verbose_name='心情关键词'),
        ),
    ]