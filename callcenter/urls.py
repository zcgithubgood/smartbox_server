# -*- coding:utf-8 -*-
__author__ = 'druid'

from . import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.Signin, name='signin'),
    url(r'^home$', views.HomePageView, name='home'),
    url(r'^formset$', views.UserInfoSetView, name='userform_default'),
    url(r'^form$', views.DefaultFormView, name='configform_default'),
    url(r'^medicinelibrary$', views.MedicineLibraryFormView, name='medicine_library'),
    url(r'^upload$', views.UploadUpgrade, name='upload'),
    url(r'^Ad$', views.AdUpload, name='Ad'),

    #url(r'^form_by_field$', views.DefaultFormByFieldView.as_view(), name='form_by_field'),
    #url(r'^form_horizontal$', views.FormHorizontalView.as_view(), name='form_horizontal'),
    #url(r'^form_inline$', views.FormInlineView.as_view(), name='form_inline'),
    #url(r'^form_with_files$', views.FormWithFilesView.as_view(), name='form_with_files'),
    #url(r'^pagination$', views.PaginationView.as_view(), name='pagination'),
    #url(r'^misc$', views.MiscView.as_view(), name='misc'),
)


urlpatterns += [
    url(r'^time/$', views.current_datetime),
    url(r'^strap_test/$', views.bootstrap_test),
    url(r'^thanks/$', views.contact_thanks),
]
