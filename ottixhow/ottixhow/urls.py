"""ottixhow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from seller_dashboard import views


urlpatterns = [
    path('admin/', admin.site.urls),
]


router = routers.DefaultRouter()
router.register(r'myproducts', views.ProductViewSet, basename='products')
router.register(r'seller', views.SellerViewSet, basename='seller')
router.register(r'vendor', views.VendorViewSet, basename='vendors')
router.register(r'competitors', views.CompetitorProductsView, basename='competitors')
router.register(r'competitor_products', views.CompetitorProductViewSet, basename='competitor_products')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('api/', include(router.urls)),
    path('', include('seller_dashboard.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.CustomAuthToken.as_view()),
    # path('api/competitors/', views.CompetitorProductsView.as_view(), name='competitors'),
    path('logout/', views.Logout.as_view()),
]
