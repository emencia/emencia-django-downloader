# -*- coding: utf-8 -*-
"""Urls for emencia.django.downloader"""
from django.conf.urls.defaults import *

from emencia.django.downloader.views import get_file, upload_progress,\
                                            upload,upload_ok

urlpatterns = patterns('',
                       url(r'^upload/progress/$', upload_progress, name='upload_progress'),
                       url(r'^upload/(?P<slug>[-\w]+)/$', upload_ok, name='upload_ok'),
                       url(r'^(?P<slug>[-\w]+)/$', get_file, name='get_file'),
                       url(r'^$', upload, name='upload'),
                       )
