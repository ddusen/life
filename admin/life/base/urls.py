from django.urls import path, re_path

from life.base.views import (index, data, chart, analytics, 
                            api_index, api_data, api_chart, 
                            api_analytics, )


urlpatterns = [
    re_path(r'^$', index),
    path('data', data),
    path('chart', chart),
    path('analytics', analytics),

    path('api/index', api_index),
    path('api/data', api_data),
    path('api/chart', api_chart),
    path('api/analytics', api_analytics),
]