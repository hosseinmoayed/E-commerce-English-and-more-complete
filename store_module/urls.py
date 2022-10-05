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
from django.contrib import admin
from django.urls import path , include

from . import views

urlpatterns = [
    path('' , views.Home , name = 'home-page'),
    path('home/category/' , views.ProductCategory , name = 'productcategory-page'),
    path('category/<slug:category>' , views.ProductList , name = 'productlist-page'),
    path('product/<slug:slug>' , views.ProductDetail.as_view() , name = 'productdetail-page'),
    path('search/' , views.search , name = 'search'),
    path('show-result/' , views.ShowResult , name = 'show-result'),
    path('add-comment/' , views.Addcomment , name = 'show-result'),
]

