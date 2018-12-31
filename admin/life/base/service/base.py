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

        return {
            'annual_consume': self.annual_consume(queryset),
        }

    def annual_consume(self, queryset):
        amount = 0
        max_amount = 0
        month_amount = 0
        consume_data = {}
        consume_data_table = []
        consume_data_pie = []
        consume_data_bar = [[], []]
        for q in queryset:
            if q['pubtime'].day == 1:
                month_amount = round(month_amount, 2)
                amount += month_amount
                consume_data_bar[0].append(month_amount)
                max_amount = month_amount if month_amount > max_amount else max_amount
                month_amount = 0
            for k, v in eval(q['consume_keywords']).items():
                month_amount += v
                if not consume_data.get(k):
                    consume_data[k] = 0
                consume_data[k] += v

        index = 0
        amount_first5 = 0 
        for k in sorted(consume_data, key=consume_data.get, reverse=True):
            value = round(consume_data[k], 2)
            consume_data_table.append({
                'icon': '/templates/static/img/%s.png' % k.lower(),
                'category': k,
                'amount': value,
            })
            consume_data_pie.append({
                'label': k,
                'value': value,
            })
            amount_first5 += value if index < 5 else 0
            index += 1

        consume_data_table = consume_data_table[:5]
        consume_data_pie = consume_data_pie[:5]
        consume_data_pie.insert(6, {
            'label': 'Others',
            'value': round(amount-amount_first5, 2),
        })
        consume_data_bar[0].reverse()
        consume_data_bar[1] = [round(max_amount+1000-consume, 2) for consume in consume_data_bar[0]]

        return {
            'consume_data_table': consume_data_table,
            'consume_data_pie': consume_data_pie,
            'consume_data_bar': consume_data_bar,
        }


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
