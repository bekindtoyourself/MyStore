"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView

from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset, AliPayView

import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token



router = DefaultRouter()

# 配置 goods 的 url
router.register('goods', GoodsListViewSet, base_name="goods")
router.register('catogorys', CategoryViewSet, base_name="catogorys")
router.register('codes', SmsCodeViewset, base_name='codes')
router.register('users', UserViewset, base_name='users')
router.register('userfavs', UserFavViewset, base_name='userfavs')
router.register('messages', LeavingMessageViewset, base_name='messages')
#收获地址
router.register('address', AddressViewset, base_name='address')
#购物车 url
router.register('shopcart', ShoppingCartViewset, base_name='shopcart')
router.register('orders', OrderViewset, base_name='orders')
#轮播图 url
router.register('banners', BannerViewset, base_name='banners')
#首页商品系列数据
router.register('indexgoods', IndexCategoryViewset, base_name='indexgoods')



urlpatterns = [
    url('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    url('doc/', include_docs_urls(title='文档')),

    url('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('', include(router.urls)),

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    #drf自带的token认证模式
    # url(r'^api-token-auth/', views.obtain_auth_token),

    # drf的认证接口
    url(r'^login/$', obtain_jwt_token),

    url(r'^apipay/return/', AliPayView.as_view(), name='alipay'),

    # 第三方登录
    url('', include('social_django.urls', namespace='social')),
]
