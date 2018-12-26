from django_extensions.management.jobs import DailyJob

from life.base.models import Brand
from life.base.service.base import RiskBrandDetailsData


class Job(DailyJob):
    # def __ini__(self):
    #     self.brand_details = RiskBrandDetailsData(params={})

    # def process(self):
    #     queryset = Brand.object.all().order_by('-score')
    #     print(queryset)

    def execute(self):
        print(1)
        # self.process()
