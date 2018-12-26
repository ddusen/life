from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from life.base.models import (Data, )
from life.utils.str_format import str_to_md5str


class DataAdmin(ImportExportActionModelAdmin):
    search_fields = ('pubtime', )
    list_display = ('pubtime', 'mood', );

admin.site.register(Data, DataAdmin) 
