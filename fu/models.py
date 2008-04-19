from django.db import models

class Author(models.Model):
    class Admin:
        pass
    first_name = models.CharField(maxlength=30)
    last_name = models.CharField(maxlength=30)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["first_name","last_name"]

    def __unicode__(self):
        return "%s %s" % (self.first_name,self.last_name)

class Issue(models.Model):
    class Admin:
        pass
    pub_date = models.DateField()
    status = models.CharField(maxlength=30,default="draft",
                              choices=(('draft','Draft'),
                                       ('published','Published')))

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date"]

    def __unicode__(self):
        return str(self.pub_date)

class Article(models.Model):
    class Admin:
        pass
    headline = models.CharField(maxlength=256)
    slug = models.SlugField(prepopulate_from=["headline"])
    lede = models.TextField(blank=True)
    content = models.TextField(blank=True)
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(Author)
    modified = models.DateTimeField(auto_now=True)
    main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        order_with_respect_to = 'issue'
        ordering = ['order']
        unique_together = [('issue','slug')]

    def __unicode__(self):
        return self.slug

    

    
    


