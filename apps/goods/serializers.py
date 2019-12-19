# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.db.models import Q

from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    # 外键反向取 model 里设置：related_name="sub_cat",
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    # bug: Got AttributeError when attempting to get a value for field `category_type` on serializer `CategorySerializer2`. The serializer field might be named incorrectly and not match any attribute or key on the `RelatedManager` instance. Original exception text was: 'RelatedManager' object has no attribute 'category_type'.
    # fixbug: 添加参数 many=True， many - If applied to a to-many relationship, you should set this argument to True.
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

# bug: TypeError at /userfavs/ The `fields` option must be a list or tuple or "__all__". Got str.
# fixbug: "fields = ('image')" to "fields = ('image',)",后面加个逗号
#  Note the comma. A tuple with only one object requires a trailing comma to distinguish it from a parenthesized object. https://stackoverflow.com/questions/36264728/django-error-the-fields-option-must-be-a-list-or-tuple-or-all
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'





# from rest_framework import serializers
# from django.db.models import Q

# from goods.models import Goods, GoodsCategory, HotSearchWords, GoodsImage, Banner
# from goods.models import GoodsCategoryBrand, IndexAd

# class CategorySerializer3(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"


# class CategorySerializer2(serializers.ModelSerializer):
#     sub_cat = CategorySerializer3(many=True)
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"


# class CategorySerializer(serializers.ModelSerializer):
#     sub_cat = CategorySerializer2(many=True)
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"


# class GoodsImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsImage
#         fields = ("image", )


# class GoodsSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     images = GoodsImageSerializer(many=True)
#     class Meta:
#         model = Goods
#         fields = "__all__"


# class HotWordsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HotSearchWords
#         fields = "__all__"


# class BannerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Banner
#         fields = "__all__"


# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsCategoryBrand
#         fields = "__all__"


# class IndexCategorySerializer(serializers.ModelSerializer):
#     brands = BrandSerializer(many=True)
#     goods = serializers.SerializerMethodField()
#     sub_cat = CategorySerializer2(many=True)
#     ad_goods = serializers.SerializerMethodField()

#     def get_ad_goods(self, obj):
#         goods_json = {}
#         ad_goods = IndexAd.objects.filter(category_id=obj.id, )
#         if ad_goods:
#             good_ins = ad_goods[0].goods
#             goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
#         return goods_json



#     def get_goods(self, obj):
#         all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
#         goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
#         return goods_serializer.data

#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"
