from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from events.views import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^$', main_page),
    
    url(r'^user/(\w+)/$',user_page),

    url(r'^login/$', 'django.contrib.auth.views.login'),

    url(r'^logout/$', logout_page),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += staticfiles_urlpatterns()
