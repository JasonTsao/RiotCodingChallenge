import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'RiotCodingChallenge.views.home', name='home'),
    # url(r'^RiotCodingChallenge/', include('RiotCodingChallenge.foo.urls')),
    url(r'^riot/api/', include('riot.urls')),
    url(r'^matches/', include('matches.urls')),
    url(r'^auth/', include('accounts.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': settings.STATIC_ROOT, 'show_indexes':True}), 
)
