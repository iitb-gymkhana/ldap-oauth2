"""sso URL Configuration

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
import re

import oauth2_provider.urls
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.views.static import serve

import account.urls
import application.urls
import resources.urls
import user_resource.urls
import widget.urls
import internal.urls

from .views import DocView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('doc/', DocView.as_view(), name='doc'),
    url(r'^doc/(?P<tab>[\w-]+\w+)/$', DocView.as_view(), name='doc'),
    path('admin/', admin.site.urls),
#    path('admin/', include((admin.site.urls, 'admin'), namespace='admin')),
    path('oauth/', include((application.urls, 'oauth'), namespace='oauth')),
    path('oauth/', include((oauth2_provider.urls, 'oauth2_provider'), namespace='oauth2_provider')),
    path('account/', include((account.urls, 'account'), namespace='account')),
    path('user/', include((user_resource.urls, 'user'), namespace='user')),
    path('resources/', include((resources.urls, 'resources'), namespace='resources')),
    path('internal/', include((internal.urls, 'internal'), namespace='internal')),
    path('widget/', include((widget.urls, 'widgets'), namespace='widgets')),
]

# Fail safe! If nginx is down, this might come handy.
#urlpatterns += [
#    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve,
#        kwargs={
#            'document_root': settings.STATIC_ROOT,
#        }
#        ),
#    url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve,
#        kwargs={
#            'document_root': settings.MEDIA_ROOT,
#        }
#        ),
#]
