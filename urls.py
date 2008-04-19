from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^fusite/', include('fusite.foo.urls')),
    (r'^$','fusite.fu.views.index'),
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)
