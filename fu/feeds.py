from fusite.fu.models import Issue,Author,Article,Comment
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "the-fu.com"
    link = "/"
    subtitle = "gameplans for dreamers"

    def items(self):
        return Article.objects.order_by("-modified")[:20]

    

class CommentFeed(Feed):
    feed_type = Atom1Feed
    title = "the-fu.com: comments"
    link = "/"
    subtitle = "gameplans for dreamers"

    def items(self):
        return Comment.objects.filter(status="approved").order_by("-timestamp")[:20]

class CommentModerationFeed(Feed):
    feed_type = Atom1Feed
    title = "the-fu.com: comments to moderate"
    link = "/"
    subtitle = "gameplans for dreamers"

    def items(self):
        return Comment.objects.filter(status="pending").order_by("-timestamp")

    
