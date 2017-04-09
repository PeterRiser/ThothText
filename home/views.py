from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from home.models import *
#create your views here.
from forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import json
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            )
            Group.objects.get(name='Reader').add(user)
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

def home(request):
    user = request.user
    books = Textbook.objects.all()
    ret = {}
    
    for o in books:
        ret[o.id] = o
    ret['books'] = books
    ret['user'] = user
    return render(request,'mainpage/home.html', ret)
    

def genpage(request, bid = -1, pid = 1):
    ret= {}
    b = Textbook.objects.get(id = int(bid))
    page = b.pages.get(page_num = int(pid))
    
        # creating an user object containing all the data
        
 
    sections = page.sections.all().order_by("order")
    
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
        'page':page,
    }
    return render(request,"content/genpage.html", ret)
  
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
    ret = {}
    query_string = ''
    found_entries = None
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
    return render(request,'mainpage/search.html', ret)


def not_in_reader_group(user):
    """Use with a ``user_passes_test`` decorator to restrict access to 
    authenticated users who are not in the "Student" group."""
    return user.is_authenticated() and not user.groups.filter(name='Reader').exists()


# Use the above with:



@login_required
@user_passes_test(not_in_reader_group, login_url='/registration/permission/')
@ensure_csrf_cookie 
def editpage(request, bid = -1, pid = 1):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    ret = {}
    b = Textbook.objects.get(id = int(bid))
    page = b.pages.get(page_num = int(pid))
    ret = {

        'book':b,
        'page':page,
        'sections':page.sections,
    }
    if request.method == 'POST':
        order = json.loads(request.POST.get("order"))
        newOrder = []
        for i in range(len(order)):
            new = Section.objects.filter(page=page).get(order=order[i])
            newOrder.append( new )
        for i in range(len(newOrder)):
            newOrder[i].order = i
            newOrder[i].save()
        newOrder[0].order = 1
        newOrder[0].save()
        
            
            
            
    return render(request,"content/editpage.html", ret)

@login_required
@user_passes_test(not_in_reader_group, login_url='/registration/permission/')
def editsection(request, bid = -1, pid=1,sid=1):
    book = Textbook.objects.get(id = int(bid))
    page = book.pages.get(page_num = int(pid))
    section = page.sections.get(order=int(sid))
    form = SectionForm(instance=section)
    ret = {
        'book':book, 
        'page':page,
        'section':section,
        'form': form
        }
   
    if request.method == 'POST':  # if the form has been filled
     
            form = SectionForm(request.POST)
     
            if form.is_valid():  # All the data is valid
                section.section_title = request.POST.get('section_title', '')
                section.text = request.POST.get('text', '')

            section.save()
            return HttpResponseRedirect('/book/'+str(book.id)+"/"+str(page.page_num)+"/editpage/")
    return render(request,"content/editsection.html", ret)

def permission(request):
    return render(request, "registration/permission.html")