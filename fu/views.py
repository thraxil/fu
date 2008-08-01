from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import Author,Issue,Article,current_issue,Comment,Tag,tag_cloud,Image
from django.core.mail import mail_managers
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    # get newest issue and redirect to it
    current = current_issue()
    if current is None:
        return HttpResponse("no published issues yet")
    else:
        return HttpResponseRedirect(current.get_absolute_url())


def issue(request,year,month,day):
    i = Issue.objects.get(pub_date="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    if i.status == "draft":
        if not request.user.is_staff():
            return HttpResponse("for staff eyes only")
    main_article = i.main_article()
    return render_to_response("issue.html",dict(issue=i,
                                                main_article=main_article,
                                                tag_cloud=tag_cloud()))

def article(request,year,month,day,slug):
    i = Issue.objects.get(pub_date="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    a = get_object_or_404(Article,issue=i,slug=slug)
    if i.status == "draft":
        if not request.user.is_staff():
            return HttpResponse("for staff eyes only")
    return render_to_response("article.html",
                              dict(issue=i,
                                   article=a,
                                   tag_cloud=tag_cloud()))

def add_comment(request,year,month,day,slug):
    i = Issue.objects.get(pub_date="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    a = list(i.article_set.filter(slug=slug))[0]

    url = request.POST.get("url","")
    if not url == "":
        if not url.startswith("http://"):
            url = "http://" + url

    if request.POST.get('name','') == "" or request.POST.get('email','') == "":
        return HttpResponse("name and email are required fields")

    if request.POST.get('content','') == "":
        return HttpResponse("no content in your comment")
    
    c = Comment(name=request.POST['name'],
                url = url,
                email = request.POST['email'],
                content = request.POST['content'],
                ip = request.META['REMOTE_ADDR'],
                article = a)
    referer = request.META.get('HTTP_REFERER',a.get_absolute_url())
    if not request.user.is_anonymous():
        c.status = "approved"
    c.save()
    if c.status == "pending":
        subject = "new comment on %s" % a.headline
        message = """comment from: %s

------
%s
------

        to approve or delete, go here:

        http://the-fu.com/admin/fu/comment/%d/
        """ % (c.name,c.content,c.id)
        mail_managers(subject,message,fail_silently=False)
        return HttpResponse("your comment has been submitted and is pending moderator approval. <a href='%s'>return</a>" % referer)
    else:
        return HttpResponseRedirect(referer)

def banner_css(request):
    current = current_issue()
    response = render_to_response("banner.html",dict(current=current))
    response['Content-Type'] = "text/css"
    return response

def team(request):
    return render_to_response("team.html",
                              dict(authors=list(Author.objects.order_by("first_name"))))


def about(request):
    return render_to_response("about.html",dict())

def links(request):
    return render_to_response("links.html",dict())

def contact(request):
    return render_to_response("contact.html",dict())

def archives(request):
    issues = Issue.objects.filter(status="published").order_by("pub_date")
    only_one = len(issues) == 1
    return render_to_response("archives.html",dict(issues=issues,only_one=only_one))

def tags(request):
    return HttpResponse("not implemented yet")

def tag(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    return render_to_response("tag.html",dict(tag=tag))

def author(request,name):
    (first,last) = name.split("_")
    author = get_object_or_404(Author,first_name=first,last_name=last)
    return render_to_response("author.html",dict(author=author))


# admin views
@login_required
def admin_index(request):
    issues = Issue.objects.all().order_by("-pub_date")    
    return render_to_response("admin_index.html",dict(issues=issues))

@login_required
def admin_image_index(request):
    return render_to_response("admin_image_index.html",dict(images=Image.objects.all().order_by("-modified")))

@login_required
def admin_image(request,id):
    return render_to_response("admin_image.html",dict(image=get_object_or_404(Image,id=id)))

@login_required
def admin_add_issue(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        pub_date = request.POST['pub_date'] # must be there
        number = request.POST["number"]
        content = request.POST.get("content","")
        author = get_object_or_404(Author,id=request.POST["author"])
        tags = request.POST.get("tags","")

        issue = Issue.objects.create(status="draft",name=name,number=number,pub_date=pub_date)

        slug = name.lower().replace(" ","-")

        article = Article.objects.create(issue=issue,
                                         headline=name,
                                         slug=slug,
                                         lede="",
                                         content=content,
                                         author=author,
                                         cardinality=1,
                                         source=request.POST.get("image_source",""),
                                         )
        
        return HttpResponseRedirect("/fuadmin/")
    else:
        all_authors = Author.objects.all()
        now = datetime.now()
        next_month = (now.year,now.month + 1,1)
        if now.month == 12:
            next_month[0] = now.year + 1
            next_month[1] = 1
        number = int(current_issue().number) + 1
        return render_to_response("admin_add_issue.html",dict(all_authors=all_authors,
                                                              number=number,
                                                              next_month="%04d-%02d-%02d" % next_month))
    
@login_required
def admin_issue(request,id):
    issue = get_object_or_404(Issue,id=id)
    return render_to_response("admin_issue.html",dict(issue=issue))


@login_required
def admin_publish_issue(request,id):
    issue = get_object_or_404(Issue,id=id)
    issue.status = "published"
    issue.save()
    return HttpResponseRedirect("/")


@login_required
def admin_edit_issue_tags(request,id):
    issue = get_object_or_404(Issue,id=id)

    for article in issue.article_set.all():
        tags = request.POST.get("tags-%d" % article.id,"")
        article.set_tags(tags)

    return HttpResponseRedirect("/fuadmin/issue/%d/" % issue.id)

