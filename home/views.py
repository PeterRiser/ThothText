from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from home.models import *
#create your views here.
def index(request):
    return render_to_response('index.html')
def genpage(request, pid = -1):
    page = Page.objects.get(id = int(pid))
    sections = page.sections.all()
    ret = {
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