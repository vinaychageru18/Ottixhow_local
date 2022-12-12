from ast import keyword
from collections import defaultdict
from unicodedata import category
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from seller_dashboard.models import Crawl
from collections import OrderedDict
from seller_dashboard.serializers import (
    ProductSerializer,
    CompetitorSerializer,
    SellerSerializer,
    VendorSerializer,
    CompetitorsSerializer
)
from seller_dashboard.models import (
    Product,
    Vendors,
    Seller,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        print(str(serializer.is_valid(raise_exception=True)))
        return Response({
            
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class VendorViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendors.objects.all()
    authentication_classes = [TokenAuthentication]

class SellerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Seller.objects.all()
    authentication_classes = [TokenAuthentication]


class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        This view should return all the users specific products
        """
        user = self.request.user
        return Product.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        from seller_dashboard.crawl_integration.models_interface import get_normalized_price
        from django.contrib.auth.models import User
        from django.shortcuts import get_object_or_404
        from django.conf import settings

        price = request.data.get('price')
        if isinstance(price, str):
            price = float(price)
        quantity = request.data.get('price')
        if isinstance(quantity, str):
            quantity = float(quantity)
        if quantity == 0.0:
            return Response({'status': 'Invalid Quantity'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        keyword = request.data.get('keyword')
        category = request.data.get('category', keyword)
        vendor_data = request.data.pop('vendor')
        seller_data = request.data.get('storename')
        request.data['vendor_name'] = vendor_data
        vendor = get_object_or_404(Vendors, name=vendor_data)
        seller = get_object_or_404(Seller, name=seller_data)
        crawl, _ = Crawl.objects.get_or_create(keyword=keyword, category=category)
        request.data['normalized_price'] = get_normalized_price(quantity=quantity, price=price)
        user = get_object_or_404(User, username=settings.DEFAULT_ADMIN)
        serializer.is_valid(raise_exception=True)
        _ = serializer.save(crawl=crawl, seller=seller, vendor=vendor, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'], name='competitors')
    def competitors(self, request, pk=None):
        params = self.request.query_params
        product_id = pk
        product = Product.objects.get(id=product_id)
        crawl = product.crawl
        competitor_products = Product.objects.filter(crawl=crawl).filter(is_best_link__in=[True])
        if query := params.get('q'):
            _on = params.get('on')
            _query_on = {
                f"{_on}__contains": query
            }
            competitor_products = competitor_products.filter(**_query_on)
        serializer = CompetitorSerializer(competitor_products, many=True, context={'request': request})
        return Response(serializer.data)

    def calculate_product_stats(self):
        """
        Returns product stats per vendor
        """
        product_stats = []
        my_products = Product.objects.filter(user=self.request.user)
        vendors = Vendors.objects.exclude(user=self.request.user)

        for vendor in vendors:
            wins = 0
            loss = 0
            for product in my_products:
                crawl = product.crawl
                competitors = Product.objects.filter(crawl=crawl).filter(is_best_link__in=[True])
                for competitor in competitors:
                    if competitor.normalized_price > product.normalized_price:
                        wins += 1
                    else:
                        loss += 1
                product_stats.append({
                    "vendor": vendor,
                    "wins": wins,
                    "loss": loss
                })
        return product_stats

    @action(detail=False, methods=['get'], name='total')
    def total(self, request):
        products = Product.objects.filter(user=request.user)
        product_stats = self.calculate_product_stats()
        wins = sum([vendor['wins'] for vendor in product_stats])
        loss = sum([vendor['loss'] for vendor in product_stats])
        return Response({'total': len(products.values_list()),
        'win': wins,
        'loss': loss})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())        
        count = queryset.count()
        brands_count = len(set([product['brands'] for product in queryset.values()]))
        category_count = len(set([product['category'] for product in queryset.values()]))
        content = {'Product Count': count,'Brand Count':brands_count,'Category Count':category_count}
        return Response(content)


    @action(detail=False, methods=['get'], name='stats')
    def products_stats(self, request):
        response = self.calculate_product_stats()
        for resp in response:
            resp['vendor'] = reverse('vendors-detail', kwargs={'pk': resp['vendor'].id})
        return Response(response)


class CompetitorProductsView(viewsets.ModelViewSet):
    """
    Returns the mapping of product and it's competitors
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    serializer_class = CompetitorsSerializer
    authentication_classes = [TokenAuthentication]
    pagination_class = StandardResultsSetPagination
    operation_description = """
    Get all products and its competitors.
    User 'q' and 'on' parameters to filter through products.
    q -> search query
    on -> which field to search on
    Example: /api/competitors?q='iphone&on=name
    """

    def get_queryset(self):
        my_products = Product.objects.filter(user=self.request.user)
        params = self.request.query_params
        if search_term := params.get('q', ''):
            search_on = params.get('on', 'name')
            _query = {
                f"{search_on}__icontains": search_term
            }
            my_products = my_products.filter(**_query)
        return my_products


    @swagger_auto_schema(operation_description=operation_description)
    @method_decorator(cache_page(60*60*2))
    def list(self, request, *args, **kwargs):
        pagination_class = StandardResultsSetPagination
        paginator = pagination_class()
        qs = list(self.get_queryset())
        page = paginator.paginate_queryset(qs, request)
        crawls = [obj.crawl for obj in page]
        competitors = list(Product.objects.exclude(user=self.request.user).filter(is_best_link__in=[True], crawl__in=crawls))
        product_list = {}
        product_list = defaultdict(list)
        for competitor in competitors:
            product_list[competitor.crawl.keyword].append(competitor)
        serializer = CompetitorsSerializer(page, many=True, context={'request': request, 'competitors': product_list})
        return paginator.get_paginated_response(serializer.data)


class CompetitorProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete']
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(PRD_IsActive=True)
