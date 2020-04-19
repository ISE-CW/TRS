"""TRS_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from TRS_backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', TemplateView.as_view(template_name="index.html")),
    # re_path(r'.*', TemplateView.as_view(template_name='index.html'))
    path('test/', views.test, name='test'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('simpleReportSet/', views.get_report_set_simple_info, name='simpleReportSet'),
    path('uploadReport/', views.upload_report, name='uploadReport'),
    path('isFeatureExist/', views.is_feature_result_exist, name='isFeatureExist'),
    path('getReportSetFeature/', views.get_report_set_feature, name='getReportSetFeature')
]
