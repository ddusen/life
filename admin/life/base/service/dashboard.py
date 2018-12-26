import random

from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from life.base.service.abstract import (Abstract, )
from life.base.models import *


class DashboardData():
    """docstring for DashboardData"""

    def get_all(self):
        months = self.get_months()
        # iri : 进口风险信息
        # ori : 出口风险信息
        # rg : 风险商品
        # rc : 风险评论
        # go : 全球概览
        # gio : 全球信息概要
        # ircs : 进口风险国家统计
        # orcs : 出口风险国家统计
        # irit : 进口风险信息变化趋势
        # orit : 出口风险信息变化趋势
        try:
            cache = Cache.objects.get(key='dashboard')
            return eval(cache.values)
        except ObjectDoesNotExist:
            return {
                'iri': self.get_iri(months),
                'ori': self.get_ori(months),
                'rg': self.get_rg(months),
                'rc': self.get_rc(months),
                'map': self.get_map(months),
                'gio': self.get_gio(),
                'ircs': self.get_ircs(),
                'orcs': self.get_orcs(),
                'irit': self.get_irit(months),
                'orit': self.get_orit(months),
            }


    #环比计算
    def mom(self, pre, cur):
        #上月
        pre_month = float(pre)
        #本月
        cur_month = float(cur)
        #同比
        if not pre_month or not cur_month:
            mom = 'Nan%'
        else:
            rate = ((cur_month / pre_month) - 1 ) * 100
            mom = '{0}%'.format(round(rate, 2))

        return cur, mom

    def get_iri(self, months):
        months = months[-2::]
        p = lambda a, b, c, d, e, x: (a.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                  + b.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                  + c.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                  + d.objects.filter(year=x[1].strftime('%Y'), month=x[1].strftime('%m')).count()
                                  + e.objects.filter(year=x[1].strftime('%Y'), month=x[1].strftime('%m')).count()
                                  )
        pre = p(Recall, OfficialRecall, EpidemicSituation, UnAgriProduct, RiskWarn, months[0])
        cur = p(Recall, OfficialRecall, EpidemicSituation, UnAgriProduct, RiskWarn, months[1])
        
        return self.mom(pre, cur)

    def get_ori(self, months):
        months = months[-2::]
        c = lambda x: ExportRiskInfo.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
        pre = c(months[0])
        cur = c(months[1])
        
        return self.mom(pre, cur)

    def get_rg(self, months):
        months = months[-2::]
        c = lambda x: Comment.objects.filter(comment_time__gte=x[0], comment_time__lt=x[1])
        rc = lambda x, y: y.filter(emotion__lt=0.4)

        comments = c(months[0])
        pre = len(self.get_risk_goods_guids(comments, rc(months[0], comments)))

        comments = c(months[1])
        cur = len(self.get_risk_goods_guids(comments, rc(months[0], comments)))

        return self.mom(pre, cur)

    def get_rc(self, months):
        months = months[-2::]
        c = lambda x: Comment.objects.filter(comment_time__gte=x[0], comment_time__lt=x[1], emotion__lt=0.4).count()
        pre = c(months[0])
        cur = c(months[1])

        return self.mom(pre, cur)

    def get_ircs(self):
        riskwarn = RiskWarn.objects.all()
        unagriproduct = UnAgriProduct.objects.all()
        total = riskwarn.count() + unagriproduct.count()

        q1 = riskwarn.values('area').annotate(dcount=Count('area')).values_list('dcount', 'area')
        q2 = unagriproduct.values('area').annotate(dcount=Count('area')).values_list('dcount', 'area')
        data = {}
        for q in q1:
            data[q[1]] = q[0]

        for q in q2:
            if not data.get(q[1]):
                data[q[1]] = q[0]

        data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:7]

        return {
            'xAxis_data': ['全球', ] + list(map(lambda d: d[0], data)),
            'series_data': [total, ] + list(map(lambda d: d[1], data)),
        }

    def get_orcs(self):
        category = Category.objects.get(name='国家地区', level=1)
        k_queryset = Keywords.objects.filter(category=category).values('guid', 'name')
        data = sorted(map(lambda k: [ExportKeywords.objects.filter(keywords=k['guid']).values(
            'export_risk_info').distinct().count(), k['name']], k_queryset), key=lambda x: x[0], reverse=True)[:7]

        return {
            'xAxis_data': ['全球', ] + list(map(lambda d: d[1], data)),
            'series_data': [ExportRiskInfo.objects.count(), ] + list(map(lambda d: d[0], data)),
        }  

    def get_irit(self, dt):
        # polymerization
        p = lambda a, b, c, d, e, x: (a.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                      + b.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                      + c.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
                                      + d.objects.filter(year=x[1].strftime('%Y'), month=x[1].strftime('%m')).count()
                                      + e.objects.filter(year=x[1].strftime('%Y'), month=x[1].strftime('%m')).count()
                                      )
        return {
            'xAxis_data': list(map(lambda d: d[1].strftime('%Y-%m'), dt)),
            'series_data': list(map(lambda d: p(Recall, OfficialRecall, EpidemicSituation, UnAgriProduct, RiskWarn, d), dt)),
        }

    def get_orit(self, dt):
        # count
        c = lambda x: ExportRiskInfo.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()

        return {
            'xAxis_data': list(map(lambda d: d[1].strftime('%Y-%m'), dt)),
            'series_data': list(map(lambda d: c(d), dt)),
        }


    def get_map(self, months):
        data = []
        start = months[-1][0]
        end = months[-1][-1]
        countries = ['韩国', '科特迪瓦', '阿富汗', '安哥拉', '阿尔巴尼亚', '阿联酋', '阿根廷', '亚美尼亚', '澳大利亚', '奥地利', '阿塞拜疆', '布隆迪', '比利时', '贝宁', '布基纳法索', '孟加拉国', '保加利亚', '巴哈马', '波斯尼亚和黑塞哥维那', '白俄罗斯', '伯利兹', '百慕大', '玻利维亚', '巴西', '文莱', '不丹', '博茨瓦纳', '中非共和国', '加拿大', '瑞士', '智利', '中国', '喀麦隆', '刚果共和国', '哥伦比亚', '哥斯达黎加', '古巴', '塞浦路斯', '捷克共和国', '德国', '吉布提', '刚果民主共和国', '丹麦', '多米尼加共和国', '多米尼克', '阿尔及利亚', '厄瓜多尔', '埃及', '厄立特里亚', '西班牙', '爱沙尼亚', '埃塞俄比亚', '芬兰', '斐济', '法国', '加蓬', '英国', '格鲁吉亚', '加纳', '几内亚', '冈比亚', '几内亚比绍', '赤道几内亚', '希腊', '格陵兰', '危地马拉', '圭亚那', '洪都拉斯', '克罗地亚', '海地', '匈牙利', '印尼', '印度', '爱尔兰', '伊朗', '伊拉克', '冰岛', '以色列', '意大利', '牙买加', '约旦', '日本', '哈萨克斯坦', '肯尼亚', '吉尔吉斯斯坦', '柬埔寨', '科索沃', '科威特', '老挝', '黎巴嫩', '利比里亚', '利比亚', '斯里兰卡', '莱索托', '立陶宛', '卢森堡', '拉脱维亚', '摩洛哥', '摩尔多瓦', '马达加斯加', '墨西哥', '马其顿', '马里', '缅甸', '黑山', '蒙古', '莫桑比克', '毛里塔尼亚', '马拉维', '马来西亚', '纳米比亚', '新喀里多尼亚', '尼日尔', '尼日利亚', '尼加拉瓜', '荷兰', '挪威', '尼泊尔', '新西兰', '阿曼', '巴基斯坦', '巴拿马', '秘鲁', '菲律宾', '巴布亚新几内亚', '波兰', '波多黎各', '葡萄牙', '巴拉圭', '卡塔尔', '罗马尼亚', '俄罗斯', '卢旺达', '西撒哈拉', '沙特阿拉伯', '苏丹', '南苏丹', '塞内加尔', '所罗门群岛', '塞拉利昂', '萨尔瓦多', '索马里', '塞尔维亚共和国', '苏里南', '斯洛伐克', '斯洛文尼亚', '瑞典', '斯威士兰', '叙利亚', '乍得', '多哥', '泰国', '塔吉克斯坦', '土库曼斯坦', '坦桑尼亚', '东帝汶', '特里尼达和多巴哥', '突尼斯', '土耳其', '乌干达', '乌克兰', '乌拉圭', '美国', '乌兹别克斯坦', '委内瑞拉', '越南', '瓦努阿图', '也门', '南非', '赞比亚', '津巴布韦', '科摩罗伊斯兰联邦共和国', '佛得角共和国', '西岸', ]

        #count country import 
        cci = lambda x, y, z : x.objects.filter(year=y.strftime('%Y'), month=y.strftime('%m'), area=z).count()

        for country in countries:
            # import risk info number
            irin = cci(UnAgriProduct, end, country, ) + cci(RiskWarn, end, country, )
           
            # export risk info number
            k = Keywords.objects.filter(name=country).values_list('guid', flat=True)
            ek = ExportKeywords.objects.filter(keywords__in=k).values_list('export_risk_info', flat=True)
            erin = ExportRiskInfo.objects.filter(pubtime__gte=start, pubtime__lt=end, guid__in=ek).count()
           
            # risk comment num
            area_label = AreaLabel.objects.filter(name=country).values_list('id', flat=True)
            brand = Brand.objects.filter(area_label__id__in=area_label).values_list('guid', flat=True)
            comments = Comment.objects.filter(comment_time__gte=start, comment_time__lt=end, goods_brand__in=brand).values('emotion', 'goods')
            riskcomments = comments.filter(emotion__lt=0.4)
            rcn = riskcomments.count()
            
            # risk goods num
            rgn = len(self.get_risk_goods_guids(comments, riskcomments))

            # risk info number
            rin = irin + erin + rgn + rcn

            data.append({
                'name': country, 
                'key': ['风险信息总数', '进口风险信息数', '出口风险信息数', '风险商品数', '风险评论数', ],
                'value': [rin, irin, erin, rgn, rcn, ]
            })

        return data

    def get_gio(self):
        days = self.get_days()
        start = days[0][0]
        end = days[-1][-1]

        #count country import 
        cci = lambda x, y : x.objects.filter(year=y.strftime('%Y'), month=y.strftime('%m')).count()
        # import risk info number
        irin = cci(UnAgriProduct, start ) + cci(RiskWarn, start )
        # export risk info number
        erin = ExportRiskInfo.objects.filter(pubtime__gte=start, pubtime__lt=end)
        # risk info number
        rin = irin + erin.count()

        # # risk comment num
        comments = Comment.objects.filter(comment_time__gte=start, comment_time__lt=end).values('comment_time', 'emotion', 'goods', )
        riskcomments = comments.filter(emotion__lt=0.4)
        rcn = riskcomments.count()
        
        # risk goods number
        rgn = len(self.get_risk_goods_guids(comments, riskcomments))

        irin_avg = irin / len(days)
        def counter(d):
            return irin_avg + erin.filter(pubtime__gte=d[0], pubtime__lt=d[1]).count() + riskcomments.filter(comment_time__gte=d[0], comment_time__lt=d[1]).count()         
        
        return {
            'irin': irin,
            'erin': erin.count(),
            'rgn': rgn,
            'rcn': rcn, 
            'xAxis_data': list(map(lambda d: d[1].strftime('%m-%d'), days)),
            'series_data': list(map(lambda d: counter(d), days))
        }

    def get_gio_by_country(self, country):
        days = self.get_days()
        start = days[0][0]
        end = days[-1][-1]

        #count country import 
        cci = lambda x, y : x.objects.filter(year=y.strftime('%Y'), month=y.strftime('%m'), area__contains=country).count()
        # import risk info number
        irin = cci(UnAgriProduct, start ) + cci(RiskWarn, start )

        # export risk info number
        k = Keywords.objects.filter(name=country).values_list('guid', flat=True)
        ek = ExportKeywords.objects.filter(keywords__in=k).values_list('export_risk_info', flat=True)
        erin = ExportRiskInfo.objects.filter(pubtime__gte=start, pubtime__lt=end, guid__in=ek)
        
        # risk info number
        rin = irin + erin.count()

        # risk comment num
        area_label = AreaLabel.objects.filter(name=country).values_list('id', flat=True)
        brand = Brand.objects.filter(area_label__id__in=area_label).values_list('guid', flat=True)
        comments = Comment.objects.filter(comment_time__gte=start, comment_time__lt=end, goods_brand__in=brand).values('comment_time', 'emotion', 'goods')
        riskcomments = comments.filter(emotion__lt=0.4)
        rcn = riskcomments.count()

        # risk goods number
        rgn = len(self.get_risk_goods_guids(comments, riskcomments))

        irin_avg = irin / len(days)
        def counter(d):
            return irin_avg + erin.filter(pubtime__gte=d[0], pubtime__lt=d[1]).count() + riskcomments.filter(comment_time__gte=d[0], comment_time__lt=d[1]).count()         
        
        return {
            'irin': irin,
            'erin': erin.count(),
            'rgn': rgn,
            'rcn': rcn, 
            'xAxis_data': list(map(lambda d: d[1].strftime('%m-%d'), days)),
            'series_data': list(map(lambda d: counter(d), days))
        }

    def get_risk_goods_guids(self, comments, riskcomments):
        if not comments or not riskcomments:
            return []
        # 风险商品: 单个商品评论总数大于 50, 且该商品小于等于0.4分的评论占该商品总评论的20%及以上
        risk_goods_guids = []
        lt04 = riskcomments.values('goods').annotate(dcount=Count('goods')).values_list('dcount', flat=True)
        for g in comments.values('goods').annotate(dcount=Count('goods')).filter(dcount__gte=50).values_list('goods', 'dcount'):
            tmp_id = g[0]
            tmp_count = lt04.filter(goods=tmp_id)
            if tmp_count and tmp_count[0] >= g[1] / 5:
                risk_goods_guids.append(tmp_id)
        return risk_goods_guids

    def get_months(self):
        minus = lambda x, y: (x + relativedelta(months=y))
        today = datetime.now().replace(day=1)
        return list(map(lambda x: [minus(today, x-11), minus(today, x-10)], range(0, 12)))

    def get_week(self):
        minus = lambda x, y: (x + timedelta(days=y)).strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now()
        return list(map(lambda x: minus(today, x-6), range(0, 7)))

    def get_days(self):
        minus = lambda x, y: (x + timedelta(days=y))
        today = datetime.now()
        return list(map(lambda x: [minus(today, x-31), minus(today, x-30),], range(0, 31, 2)))
