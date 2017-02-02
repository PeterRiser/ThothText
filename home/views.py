from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from home.models import *
#create your views here.
def index(request):
    books = Textbook.objects.all()
    ret = {}
    for o in books:
        ret[o.id] = o
    ret['books'] = books
    return render(request,'index.html', ret)
    

def genpage(request, bid = -1, pid = 1):
    b = Textbook.objects.get(id = int(bid))
    page = b.pages.get(page_num = int(pid))
    sections = page.sections.all()
    if  b.pages.filter(page_num = page.page_num+1).exists():
        next_page = page.page_num+1
    else:
        next_page = -1
    if b.pages.filter(page_num = page.page_num-1).exists():
        prev_page = page.page_num-1
    else:
        prev_page = -1
    
    ret = {
        'prev_page':prev_page,
        'next_page':next_page,
        'book':b,
        'page_title': page.page_title,
        'sections': sections,
        
    }
    return render(request,"genpage.html", ret)
    
def handler404(request):
    response = render_to_response('error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error.html', {}, 
    context_instance=RequestContext(request))
    response.status_code = 500
    return response