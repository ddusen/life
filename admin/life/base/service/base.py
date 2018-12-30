from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from life.base.models import (Data, )
from life.base.service.abstract import Abstract


class DashboardQueryset(Abstract):

    def __init__(self, params={}):
        super(DashboardQueryset, self).__init__(params)

    def get_all(self):
        fields = ('pubtime', 'consume_keywords', )

        cond = {
            'pubtime__gte': date(2018, 1, 1),
            'pubtime__lt': date(2019, 1, 1),
            # 'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Data.objects.order_by(
            '-pubtime').filter(**args).values(*fields)

        length = 0
        month_amount = 0
        consume_data = {}
        consume_data_table = []
        consume_data_pie = {}
        consume_data_bar = {'series': [[],[]], 'max': 0 }
        for q in queryset:
            if q['pubtime'].day == 1:
                month_amount = round(month_amount, 2)
                consume_data_bar['series'][0].append(month_amount)
                consume_data_bar['max'] = month_amount if month_amount > consume_data_bar['max'] else consume_data_bar['max']
                month_amount = 0
            for k, v in eval(q['consume_keywords']).items():
                month_amount+=v
                if not consume_data.get(k):
                    length += 1
                    consume_data[k] = 0
                consume_data[k] += v

        consume_data_bar['series'][0].reverse()
        consume_data_bar['series'][1] = [round(consume_data_bar['max']+1000-consume, 2) for consume in consume_data_bar['series'][0]]

        return consume_data_bar


class DataQueryset(Abstract):

    def __init__(self, params={}):
        super(DataQueryset, self).__init__(params)

    def get_all(self):
        fields = ('pubtime', 'mood', 'mood_keywords', 'consume',
                  'consume_keywords', 'time_keywords', )

        cond = {
            'pubtime__gte': date(2018, 1, 1),
            'pubtime__lt': date(2019, 1, 1),
            # 'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Data.objects.order_by(
            '-pubtime').filter(**args).values(*fields)

        return queryset
