# -*- coding: utf-8 -*-
"""Urls for emencia.django.downloader"""
from django.conf.urls.defaults import *

from emencia.django.downloader.views import get_file, upload, upload_ok, data_upload, delete_uploaded


urlpatterns = patterns('',
                       url(r'^upload/(?P<slug>[-\w]+)/$', upload_ok, name='upload_ok'),
                       url(r'^$', upload, name='upload'),
                       url(r'^ajax_upload/$', data_upload, name='ajax_upload'),
                       url(r'^delete_uploaded/(?P<file_id>[-\w]+)/$', delete_uploaded, name='delete_uploaded'),
                       url(r'^(?P<slug>[-\w]+)/$', get_file, name='get_file'),
                       )
