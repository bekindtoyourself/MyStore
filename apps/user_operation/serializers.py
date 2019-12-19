from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
import re

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer
from MxShop.settings import REGEX_MOBILE

class UserFavDetailSerializer(serializers.ModelSerializer):
    # bug:  'Goods' object is not iterable
    # fixbug: delete 'many=True'
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods', 'id')

class UserFavSerializer(serializers.ModelSerializer):
    # 设置用户为当前用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    subject = serializers.CharField(required=True)
    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    # province = serializers.CharField(required=True)
    # province = serializers.CharField(required=True)
    # city = serializers.CharField(required=True)
    # district = serializers.CharField(required=True)
    # address = serializers.CharField(required=True)
    # signer_name = serializers.CharField(required=True)
    signer_mobile = serializers.CharField(max_length=11, min_length=11, help_text='电话', label='电话')

    def validate_signer_mobile(self, signer_mobile):

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError('手机号码非法')

        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")

    # set all fields is required=True
    def get_fields(self):
        fields = super(AddressSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields