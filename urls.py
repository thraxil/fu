from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','fusite.fu.views.index'),
                       # Uncomment this for admin:
                       (r'^admin/', include('django.contrib.admin.urls')),
                       # serve media in dev mode
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/fusite/media/'}),
)
