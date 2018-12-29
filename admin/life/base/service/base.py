from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from life.base.models import (Data, )
from life.base.service.abstract import Abstract


class DataQueryset(Abstract):  # 风险品牌

    def __init__(self, params={}):
        super(DataQueryset, self).__init__(params)

    def get_all(self):
        fields = ('pubtime', 'mood', 'mood_keywords', 'consume', 'consume_keywords', 'time_keywords', )

        cond = {
            'pubtime__gte': date(2018, 1, 1),
            'pubtime__lt': date(2019, 1, 1),
            # 'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        
        queryset = Data.objects.order_by('-pubtime').filter(**args).values(*fields)

        return queryset
