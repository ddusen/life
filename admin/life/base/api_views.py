from datetime import date, timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from life.base.models import (Data, )
from life.base.service.base import (DashboardQueryset, DataQueryset, )


class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {}

    def set_params(self, params):
        for k, v in params.items():
            self.query_params[k] = v

    def paging(self, queryset, page, num):
        paginator = Paginator(queryset, num)  # Show $num <QuerySet> per page

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            results = paginator.page(paginator.num_pages)

        return results


class DashboardView(BaseView):

    def __init__(self):
        super(DashboardView, self).__init__()
    
    def set_params(self, request):
        super(DashboardView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = {
        }

        return queryset

    def get(self, request):
        self.set_params(request)

        queryset = DashboardQueryset(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class DataView(BaseView):

    def __init__(self):
        super(DataView, self).__init__()
    
    def set_params(self, request):
        super(DataView, self).set_params(request.GET)

    def paging(self, queryset):
        start = self.query_params.get('start')
        start = int(start) / 10 + 1 if start else 1
        return super(DataView, self).paging(queryset, start, self.query_params.get('length', 10))
    
    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        m = lambda x : round(float(x) * 100, 2) 
        c = lambda x : round(float(x), 1)
        def mk(items):
            mk_str = ''
            for item in items:
                mk_str += '%s%s ' % (item['prop'], item['adj'], )
            return mk_str
        def ck_or_tk(d_dict):
            k_str = ''
            for k, v in d_dict.items():
                k_str += '%s(%0.1f) ' % (k, v, )
            return k_str

        data = {
            'recordsTotal': total,
            'recordsFiltered': total,
            'data': map(lambda r: {
                 'pubtime': r['pubtime'],
                 'mood': m(r['mood']),
                 'mood_keywords': mk(eval(r['mood_keywords'])),
                 'consume': c(r['consume']),
                 'consume_keywords': ck_or_tk(eval(r['consume_keywords'])),
                 'time_keywords': ck_or_tk(eval(r['time_keywords'])),
            }, result)
        }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = DataQueryset(params=self.query_params).get_all()

        return Response(self.serialize(queryset))
