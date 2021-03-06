from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, \
    CategorySerializer, \
    BannerSerializer, \
    IndexCategorySerializer


# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet,
                       mixins.RetrieveModelMixin):
    """
    List all goods
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # bug: F:\Code\Python3\django_vue_store\MyStore\vuestore\lib\site-packages\rest_framework\pagination.py:198: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'goods.models.Goods'> QuerySet.
    # fixbug: Goods.objects.all() 更改为 queryset = Goods.objects.get_queryset().order_by('id')
    queryset = Goods.objects.get_queryset().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc', )
    ordering_fields = ['sold_num', 'shop_price', ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据，mixins.RetrieveModelMixin 获取某一条商品的详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(
        is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
