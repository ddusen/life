import random
from itertools import chain
from operator import itemgetter
from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from django.contrib.auth.models import User

from life.base.models import *
from life.base.service.abstract import Abstract
from life.utils.mysql import query


class UserData():  # 获取系统用户

    def __init__(self, user):
        self.user = user

    def get_all(self):
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_superuser', 'last_login', 'date_joined')

        queryset = User.objects.values(*fields)

        if self.user.is_active:
            if self.user.is_superuser:
                list(map(lambda x: x.update({'flag': 1}), queryset))
            else:
                q1 = queryset.exclude(id=self.user.id)
                list(map(lambda x: x.update({'flag': 0}), q1))

                q2 = queryset.filter(id=self.user.id)
                list(map(lambda x: x.update({'flag': 1}), q2))
                queryset = list(chain(q1, q2))
        else:
            list(map(lambda x: x.update({'flag': 0}), queryset))

        return queryset
