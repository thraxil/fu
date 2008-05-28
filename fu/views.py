from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import Author,Issue,Article,current_issue,Comment
from django.core.mail import mail_managers


def index(request):
    # get newest issue and redirect to it
    current = current_issue()
    if current is None:
        return HttpResponse("no published issues yet")
    else:
        return HttpResponseRedirect(current.get_absolute_url())


def issue(request,year,month,day):
    i = Issue.objects.get(pub_date="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    main_article = i.main_article()
    return render_to_response("issue.html",dict(issue=i,
                                                main_article=main_article))

def article(request,year,month,day,slug):
    i = Issue.objects.get(pub_date="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    a = list(i.article_set.filter(slug=slug))[0]
    return render_to_response("article.html",
                              dict(issue=i,
                                   article=a))

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
    issues = Issue.objects.filter(status="published").order_by("-pub_date")
    only_one = len(issues) == 1
    return render_to_response("archives.html",dict(issues=issues,only_one=only_one))


