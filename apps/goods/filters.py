# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q

from .models import Goods

# bug: django_filters:TypeError at /goods/ __init__() got an unexpected keyword argument 'name'
# fixbug: So, from django-filter==2.0 onwards, use field_name instead of name, name='shop_price' to field_name='shop_price'

class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(field_name='shop_price',lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    # bug: name 'category__parent_category__parent_category_id' is not defined
    # fixbug: return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id==value)) 之后为等号判断了，为赋值。“category__parent_category__parent_category_id=value”

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new',]



# class GoodsFilter(django_filters.rest_framework.FilterSet):
#     """
#     商品的过滤类
#     """
#     pricemin = django_filters.NumberFilter(name='shop_price', help_text="最低价格",lookup_expr='gte')
#     pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
#     top_category = django_filters.NumberFilter(method='top_category_filter')


#     def top_category_filter(self, queryset, name, value):
#         return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))


#     class Meta:
#         model = Goods
#         fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']