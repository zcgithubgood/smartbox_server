from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#import django_cron
#django_cron.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smartbox.views.home', name='home'),
    url(r'^api/', include('api.urls')),
    url(r'^callcenter/', include('callcenter.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),


    #(r'^api/v2/', include('fiber.rest_api.urls')),
    #(r'^admin/fiber/', include('fiber.admin_urls')),
    #(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('fiber',),}),
    #(r'', 'fiber.views.page'),

)
