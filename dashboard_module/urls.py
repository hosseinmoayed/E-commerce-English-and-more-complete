"""Ecommerce_Full URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('cart/', views.cart , name='cart-page'),
    path('addtocart/', views.AddtoCart , name='add-to-cart'),
    path('checkout/', views.Checkout , name='check-out-page'),
    path('remove-product/', views.RemoveProduct , name='remove-product'),
    path('coupon-apply/', views.CouponApply , name='coupon-apply'),
    path('change-count/', views.ChangeCount, name='change-count'),
    path('check-info/', views.Process_Order, name='check-info'),
    path('profile/', views.Profile, name='profile-page'),
    path('profile/order-history', views.OrderHistory, name='orderhistory-page'),
    path('profile/order-history/<pk>', views.OrderHistoryDetail, name='orderhistory-detail-page'),
    path('profile/edit-info/', views.EditInformations,  name='editing-info'),
    path('chnage-image/', views.ChangeImgae,  name='chnage-image'),
]
