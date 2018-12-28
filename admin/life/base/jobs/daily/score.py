from django_extensions.management.jobs import DailyJob


class Job(DailyJob):

    def execute(self):
    	pass