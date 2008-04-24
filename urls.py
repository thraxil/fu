from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','fusite.fu.views.index'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/$', 'fusite.fu.views.issue'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/(?P<slug>[^/]+)/$', 'fusite.fu.views.article'),                       
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/fusite/media/'}),
                       (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/fusite/data'}),                       
                       (r'^admin/', include('django.contrib.admin.urls')),
)
