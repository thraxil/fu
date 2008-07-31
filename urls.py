from django.conf.urls.defaults import *
from fusite.fu.feeds import MainFeed,CommentFeed,CommentModerationFeed

feeds = dict(main=MainFeed,
             comments=CommentFeed,
             moderation=CommentModerationFeed)

urlpatterns = patterns('',
                       (r'^$','fusite.fu.views.index'),
                       (r'^team/$','fusite.fu.views.team'),
                       (r'^team/(?P<name>[^/]+)/$','fusite.fu.views.author'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/$', 'fusite.fu.views.issue'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/(?P<slug>[^/]+)/$', 'fusite.fu.views.article'),
                       (r'^issues/(?P<year>\d+)\-(?P<month>\d+)\-(?P<day>\d+)/(?P<slug>[^/]+)/add_comment/$', 'fusite.fu.views.add_comment'),                                              
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/fusite/media/'}),
                       (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/fusite/data'}),                       
                       (r'^admin/', include('django.contrib.admin.urls')),
                       (r'^archives/', 'fusite.fu.views.archives'),                       
                       (r'^tags/$', 'fusite.fu.views.tags'),
                       (r'^tags/(?P<slug>[^/]+)/$', 'fusite.fu.views.tag'),
                       (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed', {'feed_dict': feeds}),
                       (r'^fuadmin/$','fusite.fu.views.admin_index'),
                       (r'^fuadmin/issue/(?P<id>\d+)/$','fusite.fu.views.admin_issue'),
                       (r'^fuadmin/issue/(?P<id>\d+)/publish/$','fusite.fu.views.admin_publish_issue'),                                              
                       (r'^fuadmin/add_issue/$','fusite.fu.views.admin_add_issue'),                       
                       (r'^login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^logout/$','django.contrib.auth.views.logout'),
                       (r'^accounts/password_change/$','django.contrib.auth.views.password_change'),
                       (r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done'),
                       (r'^banner.css/$',"fusite.fu.views.banner_css"),
                       
)
