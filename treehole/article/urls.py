"""treehole URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.primary_data,name=""),
    path('blog',views.primary_data2,name="blog"),
    path('write',views.primary_data3,name="write"),
    path('writearticle',views.writearticle,name="writearticle"),
    path('getmine',views.getmine,name="getmine"),
    path('search',views.search,name="search"),
    path('getall',views.getall,name="getall"),
    path('getsum',views.getsum,name="getsum"),
    path('writecomment',views.writecomment,name="writecomment"),
    path('getcomment',views.getcomment,name="getcomment"),
    path('getdetail',views.getdetail,name="getdetail"),
    path('getdate',views.getdate,name="getdate"),
    path('getauthorart',views.primary_data4,name="getauthorart"),
    path('timedata',views.timedata,name="timedata"),
    path('deletemine',views.deletemyart,name="deletemine"),
    path('modify',views.primary_data5,name="modify"),
    path('modify_art',views.modifymyart,name="modify_art"),
    path('imgupload',views.imgupload,name="imgupload"),
]