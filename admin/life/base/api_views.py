from datetime import date, timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from life.base.models import (Data, )
from life.base.service.base import (DataQueryset, )


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


class DataView(BaseView):

    def __init__(self):
        super(DataView, self).__init__()
    
    def set_params(self, request):
        super(DataView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(DataView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))
    
    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda r: {
                'pubtime': r['pubtime'],
                'mood': r['mood'],
                'mood_keywords': eval(r['mood_keywords']),
                'consume': r['consume'],
                'consume_keywords': eval(r['consume_keywords']),
                'time_keywords': eval(r['time_keywords']),
            }, result)
        }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = DataQueryset(params=self.query_params).get_all()

        return Response(self.serialize(queryset))
