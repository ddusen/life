from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from life.base.models import (Data, )


class DataAdmin(ImportExportActionModelAdmin):
    search_fields = ('pubtime', )
    list_display = ('pubtime', 'mood', 'mood_keywords', 'consume', 'consume_keywords', 'time_keywords', );

    ordering = ("-pubtime", )


admin.site.register(Data, DataAdmin) 
