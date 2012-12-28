from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render_to_response

def main_page(request):
    return render_to_response(
            'main_page.html',
            {'user':request.user,
             'head_title': u'WonderEvent',
             'page_title': u'Welcome to WonderEvent',
             'page_content': u'Where you can share events that define you!'})

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found.')
    
    events = user.event_set.all()
    template = get_template('user_page.html')
    variables = Context({
        'username': username,
        'events': events
        })
    output = template.render(variables)
    return HttpResponse(output)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
