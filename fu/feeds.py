from fusite.fu.models import Issue,Author,Article
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "the-fu.com"
    link = "/"
    subtitle = "gameplans for dreamers"

    def items(self):
        return Article.objects.order_by("-modified")[:20]

    
