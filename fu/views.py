from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import Author,Issue,Article,current_issue

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
