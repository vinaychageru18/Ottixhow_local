from django.contrib.auth.models import User
from djongo import models

from ottixhow.models import BaseOttixModel


class Vendors(BaseOttixModel):
    name = models.CharField(max_length=100)
    website_url = models.CharField(max_length=256)
    vendor_image = models.URLField(default='https://www.freeiconspng.com/uploads/no-image-icon-6.png')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)


class Seller(BaseOttixModel):
    Seller_ID = models.IntegerField(primary_key = True)
    Seller_Name =models.CharField(max_length=100)
    Loc_ID = models.FloatField()
    Seller_Rating =models.CharField(max_length=100)
    Seller_Review =models.CharField(max_length=100)



class Crawl(BaseOttixModel):
    Crawl_ID = models.IntegerField(primary_key = True)
    Crawl_Time =models.CharField(max_length=100)

class Department(BaseOttixModel):
    Dept_ID = models.IntegerField(primary_key = True)
    Dept_Name =models.CharField(max_length=100)
    Dept_Desc =models.CharField(max_length=100)
    Dept_IsActive =models.BooleanField(default=True, blank=True, null=True)
    Dept_CreatedAt = models.DateTimeField(null=True, blank=True)
    Dept_ModifiedAt = models.DateTimeField(null=True, blank=True)


class Store(BaseOttixModel):
    Store_ID = models.IntegerField(primary_key = True)
    Store_Name =models.CharField(max_length=100)
    Loc_ID = models.FloatField()
    Store_Rating =models.CharField(max_length=100)
    Store_Review =models.CharField(max_length=100)

class Location(BaseOttixModel):
    Loc_ID = models.IntegerField(primary_key = True)
    Loc_Code =models.CharField(max_length=100)
    Loc_Name =models.CharField(max_length=100)
    Loc_Zip = models.FloatField()

class Category(BaseOttixModel):
    Category_ID = models.IntegerField(primary_key = True)
    Category_Name =models.CharField(max_length=100)
    Category_Desc =models.CharField(max_length=100)
    Category_ParentID = models.FloatField()
    Category_IsActive =models.BooleanField(default=True, blank=True, null=True)
    Category_CreatedAt = models.DateTimeField(null=True, blank=True)
    Category_ModifiedAt = models.DateTimeField(null=True, blank=True)

class Competitor(BaseOttixModel):
    Competitor_ID = models.IntegerField(primary_key = True)
    Competitor_Name =models.CharField(max_length=100)
    Competitor_SalePrice = models.FloatField()
    Competitor_AvailableProducts = models.FloatField()
    Competitor_Reviews =models.CharField(max_length=100)
    Competitor_Rating =models.CharField(max_length=100)
    Competitor_Brand =models.CharField(max_length=100)
    Competitor_Category = models.ForeignKey(to=Category, on_delete=models.CASCADE, blank=True, null=True)
    Competitor_ASIN = models.FloatField()
    Competitor_UPC = models.FloatField()
    Competitor_Desc =models.CharField(max_length=100)
    Competitor_Quantity = models.FloatField()
    Competitor_UnitPrice = models.FloatField()
    Competitor_Variance = models.FloatField()
    Competitor_IsActive =models.BooleanField(default=True, blank=True, null=True)
    Competitor_CreatedAt = models.DateTimeField(null=True, blank=True)
    Competitor_ModifiedAt = models.DateTimeField(null=True, blank=True)
    Competitor_DateJoined = models.DateTimeField(null=True, blank=True)

class User(BaseOttixModel):
    User_ID = models.IntegerField(primary_key = True)
    User_Name =models.CharField(max_length=100)
    User_Email =models.CharField(max_length=100)
    User_PWD =models.CharField(max_length=100)
    User_Mobile = models.FloatField()
    User_EmailVerified =models.BooleanField(default=True, blank=True, null=True)
    User_EmailVeriCode =models.CharField(max_length=100)
    User_MobVerified =models.BooleanField(default=True, blank=True, null=True)
    User_MobileVeriCode =models.CharField(max_length=100)
    User_Grp_ID = models.FloatField()
    User_IsActive =models.BooleanField(default=True, blank=True, null=True)
    User_CreatedAt = models.DateTimeField(null=True, blank=True)
    User_ModifiedAt = models.DateTimeField(null=True, blank=True)
    User_DateJoined = models.DateTimeField(null=True, blank=True)



class Product(BaseOttixModel):
    PRD_ID = models.FloatField()
    PRD_Name = models.CharField(max_length=100)
    PRD_Desc = models.CharField(max_length=256)
    PRD_Unit = models.FloatField()
    PRD_UoM = models.FloatField()
    PRD_URL = models.CharField(max_length=256)
    PRD_UPC = models.CharField(max_length=100)
    PRD_ASIN = models.CharField(max_length=100)
    PRD_MRP = models.FloatField()
    PRD_Brand = models.CharField(max_length=100)
    Dept_ID = models.ForeignKey(to=Department, on_delete=models.CASCADE, blank=True, null=True)
    PRD_Image1 = models.BinaryField()
    PRD_Image2 = models.BinaryField()
    PRD_Image3 = models.BinaryField()
    PRD_Variance = models.CharField(max_length=100)
    Category_ID = models.ForeignKey(to=Category, on_delete=models.CASCADE, blank=True, null=True)
    #Keyword_ID = models.ForeignKey(to=Keyword, on_delete=models.CASCADE, blank=True, null=True)
    PRD_IsActive = models.BooleanField(default=True, blank=True, null=True)
    PRD_CreatedAt = models.DateTimeField(null=True, blank=True)
    PRD_ModifiedAt = models.DateTimeField(null=True, blank=True)
    User_ID = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    Competitor_ID = models.ForeignKey(to=Competitor, on_delete=models.CASCADE, blank=True, null=True)
    Store_ID = models.ForeignKey(to=Store, on_delete=models.CASCADE, blank=True, null=True)
    Seller_ID = models.ForeignKey(to=Seller, on_delete=models.CASCADE, blank=True, null=True)
    PRD_Competitor_BestLink = models.CharField(max_length=256)
    Crawl_ID = models.ForeignKey(to=Crawl, on_delete=models.CASCADE, blank=True, null=True)
    Location_ID = models.ForeignKey(to=Location, on_delete=models.CASCADE, blank=True, null=True)

class RawCrawledData(BaseOttixModel):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)


class ErrorLogs(BaseOttixModel):
    description = models.CharField(max_length=512)
    crawl = models.ForeignKey(to=RawCrawledData, on_delete=models.CASCADE)
