from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from home.models import *
#create your views here.
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def l(request):
    return HttpResponseRedirect('/')



def index(request):
    user = request.user
    books = Textbook.objects.all()
    query_string = ''
    found_entries = None
    ret = {}
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['page_title'])
        
        found_entries = Page.objects.filter(entry_query)
        ret['entry_query'] = entry_query
        if not found_entries:
            ret['found_entries'] = False
        else:
            ret['found_entries'] = found_entries
    else:
        ret['found_entries'] = False
    
    for o in books:
        ret[o.id] = o
    ret['books'] = books
    ret['user'] = user
    return render(request,'index.html', ret)
    

def genpage(request, bid = -1, pid = 1):
    ret= {}
    b = Textbook.objects.get(id = int(bid))
    page = b.pages.get(page_num = int(pid))
    if request.method == 'POST':  # if the form has been filled
 
        form = SectionForm(request.POST)
 
        if form.is_valid():  # All the data is valid
            section_title = request.POST.get('section_title', '')
            text = request.POST.get('text', '')
            page = page
            section = Section(section_title=section_title, text=text, page=page)
        # saving all the data in the current object into the database
            section.save()
        # creating an user object containing all the data
        
 
    sections = page.sections.all()
    if  b.pages.filter(page_num = page.page_num+1).exists():
        next_page = page.page_num+1
    else:
        next_page = -1
    if b.pages.filter(page_num = page.page_num-1).exists():
        prev_page = page.page_num-1
    else:
        prev_page = -1
    form = SectionForm()
    ret = {

        'prev_page':prev_page,
        'next_page':next_page,
        'book':b,
        'page_title': page.page_title,
        'sections': sections,
        'page':page,
        'form':form
    }
    return render(request,"genpage.html", ret)
  
def handler404(request):
    response = render_to_response('error.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error.html', {}, 
    context_instance=RequestContext(request))
    response.status_code = 500
    return response

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'body',])
        
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return found_entries