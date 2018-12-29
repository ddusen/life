from django.urls import path, re_path

from life.base.views import (index, data, chart, analytics, )
from life.base.api_views import(DataView, )

urlpatterns = [
    re_path(r'^$', index),
    path('data', data),
    path('chart', chart),
    path('analytics', analytics),

    path('api/index', DataView.as_view()),
    path('api/data', DataView.as_view()),
    path('api/chart', DataView.as_view()),
    path('api/analytics', DataView.as_view()),
]