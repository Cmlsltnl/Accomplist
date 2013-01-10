from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from events.views import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^$', main_page),
    
    url(r'^popular/$', popular_page),    

    url(r'^vote/$', event_vote_page),

    url(r'^tag/$', tag_cloud_page),

        # Ajax
        url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),

        url(r'^tag/([^\s]+)/$', tag_page),
    
    url(r'^user/(\w+)/$',user_page),

        url(r'^user/profile/(\w+)/$',edit_profile_page),

    url(r'^register/$', register_page),

        url(r'^register/success/$', direct_to_template,
        {'template': 'registration/register_success.html'}),

    url(r'^search/$', search_page),

    url(r'^save/$', event_save_page),

    url(r'^events/(\d+)/$', event_page),

        url(r'^event/delete/(\d+)/$', delete_event),
        # Comments
        url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login'),

     url(r'^home/$', direct_to_template,
        {'template': 'home.html'}),

    url(r'^logout/$', logout_page),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^avatar/', include('avatar.urls')),

    url(r'^messages/', include('messages.urls')),

)

urlpatterns += staticfiles_urlpatterns()
