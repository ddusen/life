from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from life.base.models import (Data, )
from life.base.service.abstract import Abstract


class DashboardQueryset(Abstract):

    def __init__(self, params={}):
        super(DashboardQueryset, self).__init__(params)

    def get_all(self):
        fields = ('pubtime', 'consume_keywords', 'mood_keywords', 'time_keywords', )

        cond = {
            'pubtime__gte': date(2018, 1, 1),
            'pubtime__lt': date(2019, 1, 1),
            # 'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Data.objects.order_by(
            '-pubtime').filter(**args).values(*fields)

        return {
            'annual_time': self.annual_time(queryset),
            'annual_consume': self.annual_consume(queryset),
            'annual_keywords': self.annual_keywords(queryset),
        }

    def annual_time(self, queryset):
        study_time_amount = 0
        study_time_month_amount = 0
        study_time_bar = [[], []]

        coding_time_amount = 0
        coding_time_month_amount = 0
        coding_time_bar = [[], []]

        fitness_time_amount = 0
        fitness_time_month_amount = 0
        fitness_time_bar = [[], []]

        sleep_time_amount = 0
        sleep_time_month_amount = 0
        sleep_time_bar = [[], []]

        year_amount = 0
        blank_year_amount = 0
        month_amount = 0
        max_month_amount = 0
        blank_month_amount = 0
        annual_time_line = [[], []]
        for q in queryset:
            if q['pubtime'].day == 1:
                month_amount = round(month_amount, 1)
                blank_month_amount = round(blank_month_amount, 1)
                study_time_month_amount = round(study_time_month_amount, 1)
                coding_time_month_amount = round(coding_time_month_amount, 1)
                fitness_time_month_amount = round(fitness_time_month_amount, 1)
                sleep_time_month_amount = round(sleep_time_month_amount, 1)

                year_amount += month_amount
                blank_year_amount += blank_month_amount
                study_time_amount += study_time_month_amount
                coding_time_amount += coding_time_month_amount
                fitness_time_amount += fitness_time_month_amount
                sleep_time_amount += sleep_time_month_amount

                max_month_amount = month_amount if month_amount > max_month_amount else max_month_amount

                annual_time_line[0].append(month_amount)
                annual_time_line[1].append(blank_month_amount)
                study_time_bar[1].append(study_time_month_amount)
                coding_time_bar[1].append(coding_time_month_amount)
                fitness_time_bar[1].append(fitness_time_month_amount)
                sleep_time_bar[1].append(sleep_time_month_amount)

                month_amount = 0
                blank_month_amount = 0
                study_time_month_amount = 0
                coding_time_month_amount = 0
                fitness_time_month_amount = 0
                sleep_time_month_amount = 0
            for k, v in eval(q['time_keywords']).items():
                if k == 'Study':
                    study_time_month_amount += v
                elif k == 'Coding':
                    coding_time_month_amount += v
                elif k == 'Fitness':
                    fitness_time_month_amount += v
                elif k == 'Sleep':
                    sleep_time_month_amount += v

                if k == 'Blank':
                    blank_month_amount += v
                else:
                    month_amount += v
        annual_time_line[0].reverse()
        annual_time_line[1].reverse()
        study_time_bar[0] = annual_time_line[0]
        study_time_bar[1].reverse()
        coding_time_bar[0] = annual_time_line[0]
        coding_time_bar[1].reverse()
        fitness_time_bar[0] = annual_time_line[0]
        fitness_time_bar[1].reverse()
        sleep_time_bar[0] = annual_time_line[0]
        sleep_time_bar[1].reverse()
        return {
            'invalid_time_rate': round(blank_year_amount / (year_amount + blank_year_amount) * 100, 0),
            'valid_time_rate': 100 - round(blank_year_amount / (year_amount + blank_year_amount) * 100, 0),
            'valid_time': annual_time_line[0],
            'invalid_time': annual_time_line[1],
            'max_amount': max_month_amount+50,
            'study_time_amount': round(study_time_amount, 0),
            'coding_time_amount': round(coding_time_amount, 0),
            'fitness_time_amount': round(fitness_time_amount, 0),
            'sleep_time_amount': round(sleep_time_amount, 0),
            'study_time_bar': study_time_bar,
            'coding_time_bar': coding_time_bar,
            'fitness_time_bar': fitness_time_bar,
            'sleep_time_bar': sleep_time_bar,
        }

    def annual_consume(self, queryset):
        amount = 0
        max_amount = 0
        month_amount = 0
        consume_data = {}
        consume_data_table = []
        consume_data_pie = []
        consume_data_bar = [[], []]
        for q in queryset:
            if q['pubtime'].day == 1:
                month_amount = round(month_amount, 2)
                amount += month_amount
                consume_data_bar[0].append(month_amount)
                max_amount = month_amount if month_amount > max_amount else max_amount
                month_amount = 0
            for k, v in eval(q['consume_keywords']).items():
                month_amount += v
                if not consume_data.get(k):
                    consume_data[k] = 0
                consume_data[k] += v

        index = 0
        amount_first5 = 0 
        for k in sorted(consume_data, key=consume_data.get, reverse=True):
            value = round(consume_data[k], 2)
            consume_data_table.append({
                'icon': '/templates/static/img/%s.png' % k.lower(),
                'category': k,
                'amount': value,
            })
            consume_data_pie.append({
                'label': k,
                'value': value,
            })
            amount_first5 += value if index < 5 else 0
            index += 1

        consume_data_table = consume_data_table[:5]
        consume_data_pie = consume_data_pie[:5]
        consume_data_pie.insert(6, {
            'label': 'Others',
            'value': round(amount-amount_first5, 2),
        })
        consume_data_bar[0].reverse()
        consume_data_bar[1] = [round(max_amount+1000-consume, 2) for consume in consume_data_bar[0]]

        return {
            'consume_data_table': consume_data_table,
            'consume_data_pie': consume_data_pie,
            'consume_data_bar': consume_data_bar,
        }

    def annual_keywords(self, queryset):
        count = 0
        prop = {}
        adj = {}
        for q in queryset:
            for mood in eval(q['mood_keywords']):
                count+=1
                p_mood = mood['prop']
                a_mood = mood['adj']
                if not a_mood:
                    continue
                prop[p_mood] = 1 if not prop.get(p_mood) else prop[p_mood]+1
                adj[a_mood] = 1 if not adj.get(a_mood) else adj[a_mood]+1

        annual_keywords_data = []
        for k in sorted(adj, key=adj.get, reverse=True):
            annual_keywords_data.append({
                'icon': '/templates/static/img/%s.png' % k,
                'keywords': k, 
                'count': adj[k], 
                'rate': round(adj[k]/count*100, 2),
            })

        return annual_keywords_data[:5]

class DataQueryset(Abstract):

    def __init__(self, params={}):
        super(DataQueryset, self).__init__(params)

    def get_all(self):
        fields = ('pubtime', 'mood', 'mood_keywords', 'consume',
                  'consume_keywords', 'time_keywords', )

        cond = {
            'pubtime__gte': date(2018, 1, 1),
            'pubtime__lt': date(2019, 1, 1),
            # 'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Data.objects.order_by(
            '-pubtime').filter(**args).values(*fields)

        return queryset
