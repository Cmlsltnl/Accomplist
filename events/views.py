from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404
from events.forms import *
from events.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage
ITEMS_PER_PAGE = 10

def main_page(request):

#TAGCLOUD 
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('?')[:10]
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].events.count()
    for tag in tags:
        tag.count = tag.events.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
           max_count = tag.count
    # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
      range = 1.0
    # Calculate tag weights.
    for tag in tags:
      tag.weight = int(
          MAX_WEIGHT * (tag.count - min_count) / range
      )

#SHAREDEVENTS
    shared_events = SharedEvent.objects.order_by('-date')[:10]
    variables = RequestContext(request, {
               'tags': tags,
               'shared_events': shared_events
    })
    return render_to_response('main_page.html', variables)

@login_required
def home_page(request):

#SHAREDEVENTS
    shared_events = SharedEvent.objects.order_by('-date')[:10]
    variables = RequestContext(request, {
               'user': request.user,
               'shared_events': shared_events,
    })
    return render_to_response('home.html', variables)



@login_required
def user_page(request, username):
    user = get_object_or_404(User, username=username)
    query_set = user.event_set.order_by('-id')
    paginator = Paginator(query_set, ITEMS_PER_PAGE)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404
    events = page.object_list
    userprofile = UserProfile.objects.get(user=user)
    variables = RequestContext(request, {
        'events': events,
        'userprofile':userprofile,
        'username': username,
        'show_tags': True,
        'show_edit': username == request.user.username,
        'show_paginator': paginator.num_pages > 1,
        'has_prev': page.has_previous(),
        'has_next': page.has_next(),
        'page': page_number,
        'pages': paginator.num_pages,
        'next_page': page_number + 1,
        'prev_page': page_number - 1
        })
    return render_to_response('user_page.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                    )
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/user/profile/%s/' % request.user.username)
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
               'registration/register.html',
               variables
    )


def _event_save(request, form):
     # Create or get instance
            instance, dummy = Instance.objects.get_or_create(
              listitem = form.cleaned_data['title']
            )
            # Create or get event.
            event, created = Event.objects.get_or_create(
              user=request.user,
              title = instance,
              description = form.cleaned_data['description']
            )
            # Update event title
          
            # Update event description.
            
            # Update event date
            
            # If the event is being updated, clear old tag list.
            if not created:
              event.tag_set.clear()
            # Create new tag list.
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                event.tag_set.add(tag)

            # Share on the main page if requested.
            if form.cleaned_data['share']:
                shared, created = SharedEvent.objects.get_or_create(
                    event=event
                )
                if created:
                    shared.users_voted.add(request.user)
                    shared.save()
            # Save event to database.
            event.save()
            return event


@login_required
def event_save_page(request):
    if request.method == 'POST':
        form = EventSaveForm(request.POST)
        if form.is_valid():
            event = _event_save(request, form)
            userprof = UserProfile.objects.get(user=request.user)
            userprof.points += 10 
            userprof.save()
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )

    elif 'title' in request.GET:
        title = request.GET['title']
        description = ''
        tags = ''
        try:
            title = Instance.objects.get(title=listitem)
            event = Event.objects.get(
            user = request.user,
            title = title
            )
            description = event.description
            tags = ' '.join(
                tag.name for tag in event.tag_set.all()
            )
        except (Instance.DoesNotExist, Event.DoesNotExist): 
            print "problem"
    else:
      form = EventSaveForm()
    variables = RequestContext(request, {
      'form': form
    })
    return render_to_response('event_save.html', variables)

def delete_event(request, id):
     u = Event.objects.filter(user = request.user).get(pk=id).delete()
     userprof = UserProfile.objects.get(user = request.user)
     userprof.points -= 20 
     userprof.save()
     return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )

def achieve_event(request,id):
    try:
     se = SharedEvent.objects.get(pk=id)
     nvotes = se.votes
    except (SharedEvent.DoesNotExist):
     nvotes = 1   
    
    u = Event.objects.filter(user=request.user).get(pk=id).delete()
    userprof = UserProfile.objects.get(user = request.user)
    userprof.points += (10*nvotes)
    userprof.save()
    return HttpResponseRedirect(
               '/user/%s/' % request.user.username
           )


def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    events = tag.events.order_by('-id')
    variables = RequestContext(request, {
        'events': events,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True
        })
    return render_to_response('tag_page.html', variables)

def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].events.count()
    for tag in tags:
        tag.count = tag.events.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
           max_count = tag.count
    # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
      range = 1.0
    # Calculate tag weights.
    for tag in tags:
      tag.weight = int(
          MAX_WEIGHT * (tag.count - min_count) / range
      )
    variables = RequestContext(request, {
               'tags': tags
    })
    return render_to_response('tag_cloud_page.html', variables)



def search_page(request):
    form = SearchForm()
    events = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                q = q & Q(title__listitem__icontains=keyword)
            form = SearchForm({'query' : query})
            events = Event.objects.filter(q)[:10]
    variables = RequestContext(request, {
         'form': form,
         'events': events,
         'show_results': show_results,
         'show_tags': True,
         'show_user': True
    })
    if request.GET.has_key('ajax'):
        return render_to_response('event_list.html', variables)
    else:
        return render_to_response('search.html', variables)


def ajax_tag_autocomplete(request):
    if 'q' in request.GET:
        tags = Tag.objects.filter(
            name__istartswith=request.GET['q']
        )[:10]
        return HttpResponse(u'\n'.join(tag.name for tag in tags))
    return HttpResponse()

@login_required
def event_vote_page(request):
    if 'id' in request.GET:
      try:
        id = request.GET['id']
        shared_event = SharedEvent.objects.get(id = id)
        user_voted = shared_event.users_voted.filter(
            username=request.user.username)
        if not user_voted:
            shared_event.votes += 1
            shared_event.users_voted.add(request.user)
            shared_event.save()

      except SharedEvent.DoesNotExist:
            raise Http404('Event not found.')  

    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect('/')        

def popular_page(request):
    today = datetime.today()
    yesterday = today - timedelta(1)
    #shared_events = SharedEvent.objects.filter(date__gt=yesterday)
    shared_events = SharedEvent.objects.order_by('-votes')[:20]
    variables = RequestContext(request, {'shared_events': shared_events})
    return render_to_response('popular_page.html', variables)

def event_page(request, event_id):
    shared_event = get_object_or_404(
    SharedEvent,id=event_id)
    variables = RequestContext(request, {
       'shared_event': shared_event})
    return render_to_response('event_page.html', variables)

@login_required
def edit_profile_page(request,username):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, username=username)
            userprof = UserProfile.objects.get(user=request.user).delete()
            userprofile, created = UserProfile.objects.get_or_create(
                user=user,
                firstName = form.cleaned_data['firstName'],
                lastName = form.cleaned_data['lastName'],
                tagline = form.cleaned_data['tagline']
                
             )
            userprofile.save()
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username)
    else:
      form = UserProfileForm()
    variables = RequestContext(request, {
            'form': form })
    return render_to_response('profile_edit.html', variables)


def leaderboard_page(request):
    userprofiles = UserProfile.objects.order_by('-points').all()
    variables = RequestContext(request, {
            'userprofiles': userprofiles })
    return render_to_response('leaderboard.html', variables)
