from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','fusite.fu.views.index'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/$', 'fusite.fu.views.issue'),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/fusite/media/'}),
                       (r'^admin/', include('django.contrib.admin.urls')),
)
