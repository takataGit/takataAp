"""
URL configuration for LearningLog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include,path

from App1.views import flontpage,LogEdit,LogRegist,CatEdit,CatRegist,LogDelete,CatDelete,ResultPage,export_csv,upload_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',flontpage, name="flontpage"),
    path('',ResultPage, name="ResultPage"),
    path("LogEdit/<slug:slug>/", LogEdit, name="LogEdit"),
    path("LogRegist/", LogRegist, name="LogRegist"),
    path("CatEdit/<slug:slug>/", CatEdit, name="CatEdit"),
    path("CatRegist/", CatRegist, name="CatRegist"),
    path('LogDelete/<slug:slug>/', LogDelete, name='LogDelete'),
    path('CatDelete/<slug:slug>/', CatDelete, name='CatDelete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('export/', export_csv, name='export_csv'), 
    path('upload/', upload_csv, name='upload_csv'),   
]
