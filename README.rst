**IMPORTANT NOTICE: This application is unmaintained and archived**

========================================
Emencia Django Emencia.django.downloader
========================================

Introduction
============

Downloader app like dl.free.fr in django

Features
========

    - upload a file and get a url for download it
    - protect download with a password (basic auth)
    - notify 3 users by mail about the upload
    - add a comment for notify users
    - send a notify mail to the sender 

Installation
============

1) With easy_install::

    # easy_install emencia.django.downloader

2) Python install::
    
    # python setup.py install

You could retrive source from the pypi or bitbucket:

    - http://bitbucket.org/rage2000/emencia.django.downloader
    - http://pypi.python.org/pypi/emencia.django.downloader

Instructions
============

    - Install the package in your python sys path
    - Add the app 'emencia.django.downloader' in the settings.py django project's file
    - Import urls into your root urls.py file:: 
    
        (r'^downloader/', include('emencia.django.downloader.urls')),

    - Add the following three applications to your INSTALLED_APPS settings
            'django.contrib.admin',
            'django.contrib.staticfiles',
            'emencia.django.downloader',

    - Set MAX_FILE_UPLOAD_SIZE setting to the maximum size of the file in bytes
    
    - If you are deploying to production, don't forget to collect static files with ./manage.py collectstatic
