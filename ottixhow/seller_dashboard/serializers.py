from rest_framework import serializers

from seller_dashboard.models import Product, Seller, Vendors, Crawl


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendors
        fields = ['*']
        #fields = ['name', 'website_url', 'vendor_image']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendors
        fields = ['*']

class SellerSerializer(serializers.HyperlinkedModelSerializer):
    vendor = VendorSerializer(read_only=True)
    class Meta:
        model = Seller
        
        fields = ['*']
        #fields = ['name', 'vendor', 'rating']


class CrawlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crawl
        fields = ['*']
        #fields = ['name', 'keyword', 'category']


class BaseProductSerializer(serializers.HyperlinkedModelSerializer):
    vendor = serializers.SerializerMethodField(source='get_vendor')

    def get_vendor(self, obj):
        return obj.vendor_name


class ProductSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ['*']
        #fields = ['id', 'name', 'description', 'price', 'department', 'brands', 'url', 'product_image', 'quantity', 'unit', 'normalized_price', 'storename', 'vendor', 'category']


class UserSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ['*']
        #fields = ['name', 'description', 'price', 'seller', 'department', 'brands', 'url', 'product_image', 'quantity', 'unit']




class SellerSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ['*']

class DepartmentSerializer(BaseProductSerializer):

        class Meta:
            model = Product
            fields = ['*']


class StoreSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ['*']
class CompetitorsSerializer(BaseProductSerializer):
    competitors = serializers.SerializerMethodField(source='get_competitors')

    class Meta:
        model = Product
        fields = ['*']


class CompetitorSerializer(BaseProductSerializer):
    competitors = serializers.SerializerMethodField(source='get_competitors')

    class Meta:
        model = Product
        fields = ['*']
        #fields = ['name', 'description', 'price','department', 'brands', 'url','product_image', 'quantity', 'unit', 'normalized_price', 'competitors', 'storename', 'vendor', 'category']
    
    def get_competitors(self, obj):
        return ProductSerializer(self.context['competitors'][obj.crawl.keyword], many=True, context=self.context).data
