from django.urls import path, re_path

from life.base.views import (index, data, analysis, )
from life.base.api_views import(DashboardView, DataView, AnalysisView, )

urlpatterns = [
    re_path(r'^$', index, name='index'),
    path('data', data, name='data'),
    path('analysis', analysis, name='analysis'),

    path('api/index', DashboardView.as_view()),
    path('api/data', DataView.as_view()),
    path('api/analysis', AnalysisView.as_view()),
]