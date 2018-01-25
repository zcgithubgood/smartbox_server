# -*- coding:utf-8 -*-
__author__ = 'druid'

from django.conf.urls import url

from . import views

from django.conf.urls import patterns, url
from django.conf import settings
#from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
#    DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView

urlpatterns = [
    # ex: /polls/
    url(r'^v1/heartbeat/$', views.heartbeat, name='heatbeart'),
    url(r'^v1/request/service/$', views.request_service, name="request_service"),
    url(r'^v1/reserve/', views.reserve, name="reserve"),
    url(r'^v1/box/info/basic/', views.basic_info, name="report_basic_info"),
    url(r'^v1/box/info/record/', views.box_record, name="report_basic_info"),
    url(r'^v1/box/info/status/', views.box_status, name="report_box_status"),
    url(r'^v1/op/$', views.get_box_operation, name="get_box_operation"),
    url(r'^v1/op/result/', views.op_result, name="report_operation_result"),
    url(r'^v1/exception/', views.exception, name="report_exception"),
    url(r'^v1/upgrade/([a-zA-Z0-9.]+)/', views.upgrade, name="upgrade"),

    url(r'^testmysql/$', views.testmysql),

]


if settings.DEBUG is False:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT}),
    ]


