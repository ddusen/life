import random
from itertools import chain
from operator import itemgetter
from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from django.contrib.auth.models import User

from life.base.models import *
from life.base.service.abstract import Abstract
from life.utils.date_format import date_format
from life.utils.mysql import query


class UserData():  # 获取系统用户

    def __init__(self, user):
        self.user = user

    def get_all(self):
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_superuser', 'last_login', 'date_joined')

        queryset = User.objects.values(*fields)

        if self.user.is_active:
            if self.user.is_superuser:
                list(map(lambda x: x.update({'flag': 1}), queryset))
            else:
                q1 = queryset.exclude(id=self.user.id)
                list(map(lambda x: x.update({'flag': 0}), q1))

                q2 = queryset.filter(id=self.user.id)
                list(map(lambda x: x.update({'flag': 1}), q2))
                queryset = list(chain(q1, q2))
        else:
            list(map(lambda x: x.update({'flag': 0}), queryset))

        return queryset


class UserAdd(Abstract):  # 添加用户

    def __init__(self, user, params={}):
        super(UserAdd, self).__init__(params)
        self.user = user

    def add_user(self):
        username = getattr(self, 'username')
        password = getattr(self, 'password')
        re_password = getattr(self, 'rePassword')
        last_name = getattr(self, 'lastName', '')
        first_name = getattr(self, 'firstName', '')
        email = getattr(self, 'email', '')

        if password != re_password:
            return -1

        if len(password) < 8:
            return -2

        if not self.user.is_active:
            return -3

        if not self.user.is_superuser:
            return -4

        try:
            User.objects.get(username=username)
            return -5
        except ObjectDoesNotExist:
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=False,
                is_active=True,
                is_superuser=False,
                last_login=datetime.now(),
                date_joined=datetime.now(),
            )
            user.set_password(password)
            user.save()
            return 1
        except Exception as e:
            print(e)
            return 0


class UserEdit(Abstract):  # 修改用户

    def __init__(self, params={}):
        super(UserEdit, self).__init__(params)

    def edit_user(self, uid):
        edit_id = uid
        username = getattr(self, 'username', None)
        last_name = getattr(self, 'lastName', None)
        first_name = getattr(self, 'firstName', None)
        new_password = getattr(self, 'newPassword', None)
        email = getattr(self, 'email', None)

        user = User.objects.get(id=edit_id)

        if new_password:
            if len(new_password) > 8:
                user.set_password(new_password)
            else:
                return -1
        try:
            if username:
                user.username = username

            if last_name:
                user.last_name = last_name

            if first_name:
                user.first_name = first_name

            if email:
                user.email = email

            user.save()
            return 1
        except Exception as e:
            print(e)
            return 0


class UserDelete(Abstract):  # 删除用户

    def __init__(self, user):
        self.user = user

    def del_user(self, uid):
        del_id = uid

        if not self.user.is_superuser:
            return -1

        try:
            User.objects.get(id=del_id).delete()
            return 1
        except Exception as e:
            print(e)
            return 0


class ExportData(Abstract):  # 出口风险信息

    def __init__(self, params):
        super(ExportData, self).__init__(params)

    def get_all(self):
        fields = ('guid', 'title', 'url', 'pubtime', 'source',)

        k_guids = getattr(self, 'keywords', None)

        if k_guids:
            k_guids_list = k_guids.split(',')
            e_guids = ExportKeywords.objects.filter(keywords__in=k_guids_list).values('export_risk_info').annotate(
                dcount=Count('export_risk_info')).filter(dcount=len(k_guids_list)).values_list('export_risk_info', flat=True)
            queryset = ExportRiskInfo.objects.filter(guid__in=e_guids)
        else:
            queryset = ExportRiskInfo.objects.all()

        cond = {
            'category': getattr(self, 'category', None),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        return queryset.filter(**args).values(*fields).order_by('-pubtime')


class IndustryData():  # 行业列表

    def get_all(self):
        industries = Industry.objects.filter(level=1)

        return map(lambda i:{
            'guid': i.guid, 
            'name': i.name, 
            'list': Industry.objects.filter(parent=i).values('guid', 'name', 'brand_num', 'risk_goods_num', 'risk_comment_num', ), 
            }, industries)
    

class BrandData(Abstract):  # 风险品牌

    def __init__(self, params={}):
        super(BrandData, self).__init__(params)

    def get_all(self):
        fields = ('guid', 'name', 'img', 'logo', 'score',
                  'area_label__name', 'area_label__label', )

        cond = {
            'name__contains': getattr(self, 'name', None),
            'area_label__id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        
        queryset = Brand.objects.filter(**args).values(*fields)

        industry_guid = getattr(self, 'industry', None)

        if industry_guid:
            brand_guids = IndustryBrand.objects.filter(industry=industry_guid).values_list('brand', flat=True)
            queryset = queryset.filter(guid__in=brand_guids)
            
        # score 品牌得分,通过评价模型计算
        queryset = sorted(queryset, key=itemgetter('score'))

        return queryset


class BrandDetailsData():  # 风险品牌详情

    def __init__(self, guid=None, guids=[]):
        self.guid = guid
        if guids:
            self.comment_queryset = Comment.objects.filter(goods_brand__in=guids)
        else:
            self.comment_queryset = Comment.objects.filter(goods_brand=guid)

    def get_all(self):
        brand_obj = Brand.objects.get(guid=self.guid)
        risk_goods = self.get_risk_goods()
        risk_comment = self.get_risk_comments().order_by('-comment_time')
        return {
            'brand_obj': brand_obj, 
            'risk_goods_num': risk_goods.count(),
            'risk_goods_list': risk_goods[0:6],
            'risk_comment_num': risk_comment.count(),
            'risk_comment_list': risk_comment[0:15],
        }

    def get_risk_goods(self):
        # 风险商品: 单个商品评论总数大于 50, 且该商品小于等于0.4分的评论占该商品总评论的20%及以上
        risk_goods_guids = []
        lt04 = self.get_risk_comments().values('goods').annotate(dcount=Count('goods')).values_list('dcount', flat=True)
        for g in self.comment_queryset.values('goods').annotate(dcount=Count('goods')).filter(dcount__gte=50).values_list('goods', 'dcount'):
            tmp_id = g[0]
            tmp_count = lt04.filter(goods=tmp_id)
            if tmp_count and tmp_count[0] >= g[1] / 5:
                risk_goods_guids.append(tmp_id)

        return Goods.objects.filter(guid__in=risk_goods_guids).values('name', 'img', 'price', 'source', 'ecommerce')

    def get_risk_comments(self):
        # 差评: emotion 0.4以下
        return self.comment_queryset.filter(emotion__lt=0.4).values('goods', 'user_name', 'comment_time', 'content')


class Select2KeywordsData(Abstract):  # 获取关键词

    def __init__(self, params):
        super(Select2KeywordsData, self).__init__(params)

    def get_all(self):
        fields = ('guid', 'name',)

        name = getattr(self, 'name', None)

        if name:
            queryset = Keywords.objects.filter(
                name__contains=name).values(*fields)
        else:
            queryset = []

        return queryset


class Select2AreaData(Abstract):  # 获取关键词

    def __init__(self, params):
        super(Select2AreaData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name',)

        name = getattr(self, 'name', None)

        if name:
            queryset = AreaLabel.objects.filter(name__contains=name).values(*fields)
        else:
            queryset = []

        return queryset


class Select2IndustryData(Abstract):  # 获取行业名称

    def __init__(self, params):
        super(Select2IndustryData, self).__init__(params)

    def get_all(self):
        fields = ('guid', 'name',)

        name = getattr(self, 'name', None)

        if name:
            queryset = Industry.objects.filter(name__contains=name).values(*fields)
        else:
            queryset = []

        return queryset


class RecallData(Abstract):

    def __init__(self, params):
        super(RecallData, self).__init__(params)

    def get_all(self):
        fields = ('title', 'url', 'pubtime', )

        cond = {
            'title__contains': getattr(self, 'title', None),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Recall.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class OfficialRecallData(Abstract):

    def __init__(self, params):
        super(OfficialRecallData, self).__init__(params)

    def get_all(self):
        fields = ('title', 'url', 'pubtime', )

        cond = {
            'title__contains': getattr(self, 'title', None),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = OfficialRecall.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class EpidemicSituationData(Abstract):

    def __init__(self, params):
        super(EpidemicSituationData, self).__init__(params)

    def get_all(self):
        fields = ('title', 'url', 'pubtime', )

        cond = {
            'title__contains': getattr(self, 'title', None),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = EpidemicSituation.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class UnAgriProductData(Abstract):

    def __init__(self, params):
        super(UnAgriProductData, self).__init__(params)

    def get_all(self):
        fields = ('number', 'hscode', 'product', 'area', 'scale', 'cause', 'judg_basis',
                  'measure', 'process_basis', 'p_number', 'e_number', 'port', 'year', 'month', )

        cond = {
            'number__contains': getattr(self, 'number', None),
            'hscode__contains': getattr(self, 'hscode', None),
            'product__contains': getattr(self, 'product', None),
            'area__contains': getattr(self, 'area', None),
            'scale__contains': getattr(self, 'scale', None),
            'cause__contains': getattr(self, 'cause', None),
            'judg_basis__contains': getattr(self, 'judgBasis', None),
            'measure__contains': getattr(self, 'measure', None),
            'process_basis__contains': getattr(self, 'processBasis', None),
            'p_number__contains': getattr(self, 'pNumber', None),
            'e_number__contains': getattr(self, 'eNumber', None),
            'port__contains': getattr(self, 'port', None),
            'year': getattr(self, 'year', None),
            'month': getattr(self, 'month', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = UnAgriProduct.objects.filter(
            **args).values(*fields).order_by('-year')

        return queryset


class RiskWarnData(Abstract):

    def __init__(self, params):
        super(RiskWarnData, self).__init__(params)

    def get_all(self):
        fields = ('number', 'hscode', 'product', 'area', 'e_info', 'i_info',
                  'i_number', 'scale', 'cause', 'port', 'year', 'month', 'category',)

        cond = {
            'number__contains': getattr(self, 'number', None),
            'hscode__contains': getattr(self, 'hscode', None),
            'product__contains': getattr(self, 'product', None),
            'area__contains': getattr(self, 'area', None),
            'e_info__contains': getattr(self, 'eInfo', None),
            'i_info__contains': getattr(self, 'iInfo', None),
            'i_number__contains': getattr(self, 'iNumber', None),
            'scale__contains': getattr(self, 'scale', None),
            'cause__contains': getattr(self, 'cause', None),
            'port__contains': getattr(self, 'port', None),
            'year': getattr(self, 'year', None),
            'month': getattr(self, 'month', None),
            'category': getattr(self, 'category', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = RiskWarn.objects.filter(
            **args).values(*fields).order_by('-year')

        return queryset


class ChartsImportData(Abstract):
    """docstring for ChartsImportData"""

    def __init__(self, params):
        super(ChartsImportData, self).__init__(params)

    def get_charts(self):
        chart_type = getattr(self, 'type', None)

        # Imported substandard agricultural products 进口不合格农产品
        # Import food risk warning 进口食品风险预警
        # Import cosmetics risk information 进口化妆品风险信息
        # Number of defective products 缺陷产品数目
        # The number of product recalls 产品召回数目
        if 'isap' == chart_type:
            return self.get_isap()
        elif 'ifrw' == chart_type:
            return self.get_ifrw()
        elif 'icri' == chart_type:
            return self.get_icri()
        elif 'nodp' == chart_type:
            return self.get_nodp()
        elif 'tnopr' == chart_type:
            return self.get_tnopr()
        else:
            return []

    def get_isap(self):
        queryset = UnAgriProduct.objects.values('area').annotate(dcount=Count('area')).order_by('-dcount')[:5:]

        return map(lambda q: {'value': q['dcount'],
                              'name': q['area']}, queryset)

    def get_ifrw(self):
        queryset = RiskWarn.objects.filter(category=1).values('area').annotate(dcount=Count('area')).order_by('-dcount')[:5:]

        return map(lambda q: {'value': q['dcount'],
                              'name': q['area']}, queryset)

    def get_icri(self):
        queryset = RiskWarn.objects.filter(category=2).values('area').annotate(dcount=Count('area')).order_by('-dcount')[:5:]

        return map(lambda q: {'value': q['dcount'],
                              'name': q['area']}, queryset)

    def get_nodp(self):
        months = self.get_months()
        return {'data': map(lambda q: OfficialRecall.objects.filter(
                                                                pubtime__year=q.split('-')[0], 
                                                                pubtime__month=q.split('-')[1]
                                                            ).count(), months),
                'series': [{
                    'data': months,
                    'type': 'bar',
                }],
                }

    def get_tnopr(self):
        months = self.get_months()
        return {'data':map(lambda q: Recall.objects.filter(
                                                                pubtime__year=q.split('-')[0], 
                                                                pubtime__month=q.split('-')[1]
                                                            ).count(), months),
                'series': [{
                    'data': months,
                    'type': 'bar',
                }],
                }

    def get_months(self):
        now = date.today()
        one = now
        two = now + timedelta(-1*365/12)
        three = now + timedelta(-2*365/12)
        four = now + timedelta(-3*365/12)
        five = now + timedelta(-4*365/12)
        six = now + timedelta(-5*365/12)

        return(
            six.strftime("%Y-%m"),
            five.strftime("%Y-%m"),
            four.strftime("%Y-%m"),
            three.strftime("%Y-%m"),
            two.strftime("%Y-%m"),
            one.strftime("%Y-%m"),
            )


class ChartsExportData(Abstract):
    """docstring for ChartsExportData"""

    def __init__(self, params):
        super(ChartsExportData, self).__init__(params)

    def get_charts(self):
        chart_type = getattr(self, 'type', None)

        # Information category accounted for 信息类别占比
        # Export country risk information proportion 出口国风险信息占比
        # The proportion of event action 事件动作占比
        # The number of risks changes 风险数目变化
        if 'icaf' == chart_type:
            return self.get_icaf()
        elif 'ecrip' == chart_type:
            return self.get_ecrip()
        elif 'tpoea' == chart_type:
            return self.get_tpoea()
        elif 'tnorc' == chart_type:
            return self.get_tnorc()
        else:
            return []

    def get_icaf(self):
        queryset = ExportRiskInfo.objects.all()
        return {
            'data': [
                {'value': queryset.filter(
                    category='1').count(), 'name': 'TBT'},
                {'value': queryset.filter(
                    category='2').count(), 'name': 'SPS'},
                {'value': queryset.filter(
                    category='3').count(), 'name': '召回信息'},
                {'value': queryset.filter(
                    category='4').count(), 'name': '风险信息'},
            ],
        }

    def get_ecrip(self):
        category = Category.objects.get(name='国家地区', level=1)
        k_queryset = Keywords.objects.filter(category=category).values('guid', 'name')[:5:]
        return {'data': map(lambda k: {
            'value': ExportKeywords.objects.filter(
                        keywords=k['guid']).values('export_risk_info').distinct().count(), 
            'name': k['name']}, k_queryset)}

    def get_tpoea(self):
        c_queryset = Category.objects.filter(level=2).values('id', 'name',)
        return {'data': map(lambda c: {
            'value': ExportKeywords.objects.filter(
                        keywords__in=Keywords.objects.filter(
                            category__id=c['id']).values_list('guid', flat=True)).values('export_risk_info').distinct().count(), 
            'name': c['name']}, c_queryset)}

    def get_tnorc(self):
        e_querset = ExportRiskInfo.objects.all()
        now = datetime.now()
        one = now
        two = now + timedelta(days=-1)
        three = now + timedelta(days=-2)
        four = now + timedelta(days=-3)
        five = now + timedelta(days=-4)
        six = now + timedelta(days=-5)
        serven = now + timedelta(days=-6)
        return {
                  'data': [
                     serven.strftime('%Y-%m-%d'),
                     six.strftime('%Y-%m-%d'),
                     five.strftime('%Y-%m-%d'),
                     four.strftime('%Y-%m-%d'),
                     three.strftime('%Y-%m-%d'),
                     two.strftime('%Y-%m-%d'),
                     one.strftime('%Y-%m-%d'),
                    ],
                  'series': [
                    {
                      'name': '全部',
                      'type': 'line',
                      'data': [
                        e_querset.filter(pubtime=serven).count(), 
                        e_querset.filter(pubtime=six).count(), 
                        e_querset.filter(pubtime=five).count(), 
                        e_querset.filter(pubtime=four).count(), 
                        e_querset.filter(pubtime=three).count(), 
                        e_querset.filter(pubtime=two).count(), 
                        e_querset.filter(pubtime=one).count(), 
                      ],
                    },
                    {
                      'name': 'TBT',
                      'type': 'line',
                      'data': [
                        e_querset.filter(category='1', pubtime=serven).count(), 
                        e_querset.filter(category='1', pubtime=six).count(), 
                        e_querset.filter(category='1', pubtime=five).count(), 
                        e_querset.filter(category='1', pubtime=four).count(), 
                        e_querset.filter(category='1', pubtime=three).count(), 
                        e_querset.filter(category='1', pubtime=two).count(), 
                        e_querset.filter(category='1', pubtime=one).count(), 
                      ],
                    },
                    {
                      'name': 'SPS',
                      'type': 'line',
                      'data': [
                        e_querset.filter(category='2', pubtime=serven).count(), 
                        e_querset.filter(category='2', pubtime=six).count(), 
                        e_querset.filter(category='2', pubtime=five).count(), 
                        e_querset.filter(category='2', pubtime=four).count(), 
                        e_querset.filter(category='2', pubtime=three).count(), 
                        e_querset.filter(category='2', pubtime=two).count(), 
                        e_querset.filter(category='2', pubtime=one).count(), 
                      ],
                    },
                    {
                      'name': '召回信息',
                      'type': 'line',
                      'data': [
                        e_querset.filter(category='3', pubtime=serven).count(), 
                        e_querset.filter(category='3', pubtime=six).count(), 
                        e_querset.filter(category='3', pubtime=five).count(), 
                        e_querset.filter(category='3', pubtime=four).count(), 
                        e_querset.filter(category='3', pubtime=three).count(), 
                        e_querset.filter(category='3', pubtime=two).count(), 
                        e_querset.filter(category='3', pubtime=one).count(), 
                      ],
                    },
                    {
                      'name': '风险信息',
                      'type': 'line',
                      'data': [
                        e_querset.filter(category='4', pubtime=serven).count(), 
                        e_querset.filter(category='4', pubtime=six).count(), 
                        e_querset.filter(category='4', pubtime=five).count(), 
                        e_querset.filter(category='4', pubtime=four).count(), 
                        e_querset.filter(category='4', pubtime=three).count(), 
                        e_querset.filter(category='4', pubtime=two).count(), 
                        e_querset.filter(category='4', pubtime=one).count(), 
                      ],
                    },
                  ],
                }


class ChartsEcommerceData(Abstract):
    """docstring for ChartsEcommerceData"""

    def __init__(self, params):
        super(ChartsEcommerceData, self).__init__(params)

    def get_charts(self):
        chart_type = getattr(self, 'type', None)

        # Imported substandard agricultural products 进口不合格农产品
        # Import food risk warning 进口食品风险预警
        # Import cosmetics risk information 进口化妆品风险信息
        # Number of defective products 缺陷产品数目
        # The number of product recalls 产品召回数目
        if 'isap' == chart_type:
            return self.get_isap()
        elif 'ifrw' == chart_type:
            return self.get_ifrw()
        elif 'icri' == chart_type:
            return self.get_icri()
        elif 'nodp' == chart_type:
            return self.get_nodp
        elif 'tnopr' == chart_type:
            return self.get_tnopr()
        else:
            return []

    def get_isap(self):
        queryset = UnAgriProduct.objects.values(
            'area').annotate(dcount=Count('area'))
        return queryset
