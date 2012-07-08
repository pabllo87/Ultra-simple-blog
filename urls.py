from django.conf.urls.defaults import *
from django.contrib import admin
from blog.views import view, list

handler500 = 'djangotoolbox.errorviews.server_error'

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^tinymce/$', include('tinymce.urls')),
    url(r'^lists/(?P<slug>[\w_-]+)/$', list, name='blog_list'),
    url(r'^(?P<slug>[\w_-]+)/$', view, name='blog_view'),
)
