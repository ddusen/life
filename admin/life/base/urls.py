from django.urls import path, re_path

from life.base.views import (index, data, analytics, )
from life.base.api_views import(DashboardView, DataView, )

urlpatterns = [
    re_path(r'^$', index, name='index'),
    path('data', data, name='data'),
    path('analytics', analytics, name='analytics'),

    path('api/index', DashboardView.as_view()),
    path('api/data', DataView.as_view()),
    path('api/analytics', DataView.as_view()),
]