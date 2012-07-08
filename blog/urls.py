# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from blog.views import *

urlpatterns = patterns('',
    url(r'^lists/(?P<slug>[\w_-]+)/$', list, name='blog_list'),
    url(r'^(?P<slug>[\w_-]+)/$', view, name='blog_view'),
)