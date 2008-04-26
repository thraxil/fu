from django.conf.urls.defaults import *
from fusite.fu.feeds import MainFeed

feeds = dict(main=MainFeed)

urlpatterns = patterns('',
                       (r'^$','fusite.fu.views.index'),
                       (r'^roster/$','fusite.fu.views.roster'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/$', 'fusite.fu.views.issue'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/(?P<slug>[^/]+)/$', 'fusite.fu.views.article'),                       
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/fusite/media/'}),
                       (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/fusite/data'}),                       
                       (r'^admin/', include('django.contrib.admin.urls')),
                       (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
