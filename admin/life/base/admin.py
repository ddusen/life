from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from life.base.models import (Data, )


class DataAdmin(ImportExportActionModelAdmin):
    search_fields = ('pubtime', )
    list_display = ('pubtime', 'mood', 'keywords' );

admin.site.register(Data, DataAdmin) 
