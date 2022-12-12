from django.contrib import admin

from seller_dashboard.models import (
    Crawl, Product, Vendors, RawCrawledData, ErrorLogs, Seller, Store, Location, User, Department,Category,Competitor
)

# Register your models here.
admin.site.register([Crawl, Product, Vendors, RawCrawledData, ErrorLogs, Seller, Store, Location, User, Department,Category,Competitor])
