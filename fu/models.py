from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
import re

class Author(models.Model):
    class Admin:
        pass
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    headshot = ImageWithThumbnailsField(upload_to="headshots",
                                        thumbnail = {
        'size' : (65,65)
        },
                                        extra_thumbnails={
        'admin': {
        'size': (70, 50),
        'options': ('sharpen',),
        }
        }
                                        )

    class Meta:
        ordering = ["first_name","last_name"]

    def __str__(self):
        return "%s %s" % (self.first_name,self.last_name)

    def fullname(self):
        return "%s %s" % (self.first_name,self.last_name)


def current_issue():
    r = Issue.objects.filter(status="published").order_by("-pub_date")
    if r.count() == 0:
        return None
    else:
        return list(r)[0]

class Issue(models.Model):
    class Admin:
        pass
    pub_date = models.DateField()
    status = models.CharField(max_length=30,default="draft",
                              choices=(('draft','Draft'),
                                       ('published','Published')))

    banner = ImageWithThumbnailsField(upload_to="banners",
                                      thumbnail = {
        'size' : (700,100)
        },
                                      extra_thumbnails={
        'admin': {
        'size': (70, 50),
        'options': ('sharpen',),
        }
        },
                                      blank=True
                                      )

    name = models.CharField(max_length=256)
    number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date"]

    def __str__(self):
        return str(self.pub_date)

    def get_absolute_url(self):
        return "/issues/%04d-%02d-%02d/" % (self.pub_date.year,self.pub_date.month,self.pub_date.day)

    def non_main_articles(self):
        return list(self.article_set.order_by("cardinality"))[1:]

    def main_article(self):
        return list(self.article_set.order_by("cardinality"))[0]

    def is_current(self):
        return self == current_issue()

    def banner_url(self):
        return "/uploads/banners/%04d-%02d-%02d.jpg" % (self.pub_date.year,self.pub_date.month,self.pub_date.day)

class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(prepopulate_from=["name"])

    class Admin:
        pass

    def get_absolute_url(self):
        return "/tags/%s/" % self.slug

    def __str__(self):
        return self.name

def make_slug(title="no title"):
    title = title.strip()
    slug = re.sub(r"[\W\-]+","-",title)
    slug = re.sub(r"^\-+","",slug)
    slug = re.sub(r"\-+$","",slug)
    if slug == "":
        slug = "-"
    return slug

def get_or_create_tag(name):
    r = Tag.objects.filter(name__iexact=name)
    if r.count() > 0:
        return r[0]
    else:
        return Tag.objects.create(name=name,slug=make_slug(name))


def tag_cloud():
    """ eventually, we'll scale the cloud. for now, just return list of all tags """
    return Tag.objects.all().order_by("name")

def clear_unused_tags():
    for t in Tag.objects.all():
        if t.article_set.all().count() == 0:
            t.delete()


class Article(models.Model):
    headline = models.CharField(max_length=256)
    slug = models.SlugField(prepopulate_from=["headline"])
    lede = models.TextField(blank=True)
    content = models.TextField(blank=True)
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(Author)
    modified = models.DateTimeField(auto_now=True)
    cartoon = models.BooleanField(default=False)
    cardinality = models.PositiveSmallIntegerField(default=1)
    image = ImageWithThumbnailsField(upload_to="article_images/%Y/%m/%d",
                                     thumbnail = {
        'size' : (200,200)
        },
                                     extra_thumbnails={
        'admin': {
        'size': (70, 50),
        'options': ('sharpen',),
        }
        },
                                     blank=True
                                     )
    source = models.CharField("Image source",max_length=256,blank=True)
    tags      = models.ManyToManyField(Tag,filter_interface=models.HORIZONTAL,blank=True)
    atype = models.CharField("Type",max_length=30,default="article",
                             choices=(('article','Article'),
                                      ('photos','Photos'),
                                      ('cartoon','Cartoon')))

    
    class Admin:
        list_filter = ["issue"]

    class Meta:
        order_with_respect_to = 'issue'
        ordering = ['cardinality']
        unique_together = [('issue','slug')]

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return "%s%s/" % (self.issue.get_absolute_url(),self.slug)

    def approved_comments(self):
        return self.comment_set.filter(status="approved").order_by("timestamp")

    def tags_string(self):
        return ", ".join([t.name.lower() for t in self.tags.all()])

    def set_tags(self,tags_string):
        self.tags.clear()
        for tag in tags_string.split(","):
            tag = tag.lower().strip()
            if not tag:
                continue
            t = get_or_create_tag(tag)
            self.tags.add(t)
        clear_unused_tags()
        return

    def is_cartoon(self):
        return self.atype == "cartoon"




class Comment(models.Model):
    article = models.ForeignKey(Article)
    name    = models.CharField(max_length=256)
    email   = models.EmailField()
    url     = models.URLField(blank=True)
    ip      = models.IPAddressField()
    status  = models.CharField(max_length=30,default="pending",
                               choices=(('pending','Pending Moderation'),
                                        ('approved','Approved')))
    timestamp = models.DateTimeField(auto_now_add=True)
    content   = models.TextField()


    class Admin:
        list_filter = ["status"]

    class Meta:
        order_with_respect_to = 'article'
        ordering = ['timestamp']

    def __str__(self):
        return "[%s] on %s by %s at %s" % (self.status,self.article.headline,self.name,self.timestamp)

    def get_absolute_url(self):
        return self.article.get_absolute_url() + "#comment-%s" % str(self.id)




    

    
    


