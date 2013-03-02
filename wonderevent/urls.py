from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from events.views import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.conf.urls.defaults import *
from events.api import *
from tastypie.api import Api
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(InstanceResource());
v1_api.register(UserResource());
v1_api.register(EventResource());
v1_api.register(SharedEventResource());
v1_api.register(TagResource());
v1_api.register(UserProfileResource());


urlpatterns = patterns('',
    
    url(r'^api/',include(v1_api.urls)),

    url(r'^$', main_page),
    
    url(r'^popular/$', popular_page),    

    url(r'^vote/$', event_vote_page),

    url(r'^tag/$', tag_cloud_page),

    url(r'^leaderboards/$',leaderboard_page),

        # Ajax
        url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),

        url(r'^tag/([^\s]+)/$', tag_page),
    
    url(r'^user/(\w+)/$',user_page),

        url(r'^user/profile/(\w+)/$',edit_profile_page),

        url(r'^settings/user$',direct_to_template, {'template': 'settings/settings.html'}),

        url(r'^settings/user/password/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/settings/user/password-changed'}),

        url(r'^settings/user/password-changed$', direct_to_template, {'template': 'registration/password_change_done.html'}),
    
        url(r'^register/$', register_page),

        url(r'^register/success/$', direct_to_template,
        {'template': 'registration/register_success.html'}),

    url(r'^search/$', search_page),

    url(r'^save/$', event_save_page),

    url(r'^events/(\d+)/$', event_page),

        url(r'^event/delete/(\d+)/$', delete_event),

        url(r'^event/achieve/(\d+)/$', achieve_event),
        # Comments
        url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login'),

     url(r'^home/$', home_page),

    url(r'^logout/$', logout_page),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    

    

)
