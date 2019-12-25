# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q

from .models import Goods

# bug: django_filters:TypeError at /goods/ __init__() got an unexpected keyword argument 'name'
# fixbug: So, from django-filter==2.0 onwards, use field_name instead of name, name='shop_price' to field_name='shop_price'


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(
        field_name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(
        field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(
        method='top_category_filter', field_name='top_category')

    # bug: name 'category__parent_category__parent_category_id' is not defined
    # fixbug: return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id==value)) 之后为等号判断了，为赋值。“category__parent_category__parent_category_id=value”


# QuerySet如果跨表查询呢？
# 我们知道对象跨表查询可以用点,QuerySet可以使用双下划线“__”，例如获取Uhost表中所有对象的project id 和project name，可以这样做：host2 = Uhost.objects.all().values('ip','name','project__id','project__name')
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
