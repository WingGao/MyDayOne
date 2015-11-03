"""MyDayOne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^init_dayone', 'Dayone.views.init_dayone_entries'),
    url(r'^entry/list', 'Dayone.views.all_entries'),
    url(r'^entry/search', 'Dayone.views.search'),
    url(r'^entry/([0-9A-Z]{32})$', 'Dayone.views.entry'),
    url(r'^photo/([0-9A-Z]{32})$', 'Dayone.views.photo'),
    url(r'^tag/all', 'Dayone.views.all_tags'),
    url(r'^tag/(.*?)$', 'Dayone.views.one_tag'),
    url(r'^day/all', 'Dayone.views.all_days'),
    url(r'^howto', 'Dayone.views.howto'),
]
