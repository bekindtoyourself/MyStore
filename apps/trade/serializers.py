# -*- coding: utf-8 -*-
__author__ = 'bobby'

import time
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path

# bug: object() takes no parameters
# fixbug: 'class ShopCartDetailSerializer():' 添加 参数 -> class ShopCartDetailSerializer(serializers.ModelSerializer):

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')

class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value": "商品数量不能小于一",
        "required": "请选择购买数量"
        })
    # 外键都是正向取得 
    # serializers.Serializer PrimaryKeyRelatedField
    # serializers.ModelSerializer images = GoodsImageSerializer(many=True)
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        goods = validated_data['goods']
        nums = validated_data['nums']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        
        # bug: list index out of range \django\db\models\query.py
        # fixbug: 'existed[0]' isn't exist. 注释掉
        # print('existed: ', existed[0])

        # bug :'QuerySet' object has no attribute 'nums'
        # fixbug: add "existed = existed[0]"
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    # 某个字段不属于指定model，它是read_only，只需要将它序列化传递给用户，但是在这个model中，没有这个字段！我们需要用到SerializerMethodField。
    alipay_url = serializers.SerializerMethodField(read_only=True)

    # 方法写法：get_ + 字段
    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )

        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url    


    def generate_order_sn(self):
        from random import randint
        order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%W"), user_id=self.context["request"].user.id, ran_str=randint(10, 99))
        return order_sn

    # bug: "order_sn": "<bound method OrderSerializer.", order_sn 变成这样
    # fixbug: "self.generate_order_sn" 改为 "self.generate_order_sn()"
    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
        