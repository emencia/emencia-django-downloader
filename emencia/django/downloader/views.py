# -*- coding: utf-8 -*-
"""views for emencia.django.downloader"""
import mimetypes
import base64
import logging
import datetime
try:
    import json
except:
    import simplejson as json

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.conf import settings
from django.middleware.csrf import get_token

from emencia.django.downloader.models import Download, UploadedFile, DownloadGroup
from emencia.django.downloader.forms import ShareForm, UploadForm


def get_file(request, slug):
    """
    Retrieve the uploaded file by the slug
    """
    download = get_object_or_404(Download, slug=slug)
    get_file = True
    if download.password != '':
        get_file = False
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                # NOTE: We are only support basic authentication for now
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                    if passwd == download.password:
                        get_file = True

    if not get_file:
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="password"'
    else:
        try:
            mimetype = mimetypes.types_map[".%s" % download.filename().split('.')[-1]]
        except KeyError:
            mimetype = 'application/octet-stream'
        response = HttpResponse(download.file.file.read(), mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % download.filename()
    return response


def upload_ok(request, slug):
    """
    Display the confirmation page
    """
    download = get_object_or_404(DownloadGroup, slug=slug)
    data = {
        'download_group': download,
        'host': request.get_host(),
    }
    return render_to_response('downloader/upload_ok.html', data, RequestContext(request))


def upload(request):
    """
    Process notifications
    """
    if request.method == 'POST':
        form = ShareForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info("Upload form is valid: %s" % form)
            download = form.save()
            logging.info("Saved upload: %s" % upload)
            host = request.get_host()
            sender_mail = form.cleaned_data['my_mail']
            context = Context({'download_group': download,
                               'host': request.get_host(),
                               'sender': sender_mail,
                               'comment': form.cleaned_data['comment']
                              })
            if sender_mail != '':
                template = get_template('downloader/notify_sender.txt')
                send_mail("Confirmation de notification d'envoi de fichier via %s" % host,
                          template.render(context), 'notify@emencia.com',
                          (sender_mail,),
                          fail_silently=False)
            notify_mails = [mail for mail in (form.cleaned_data['notify1'],
                                              form.cleaned_data['notify2'],
                                              form.cleaned_data['notify3']) \
                                              if mail != '']
            template = get_template('downloader/notify_friends.txt')
            send_mail("Notification d'envoi de fichier via %s" % host,
                      template.render(context), 'notify@emencia.com',
                      notify_mails,
                      fail_silently=False)
            return HttpResponseRedirect(reverse('upload_ok',
                                        args=[download.slug]))


        else:
            logging.error("invalid form: %s" % form)
            logging.error("form errors: %s" % form.errors)

    else:
        form = ShareForm()

    data = {
        'form': form,
        'csrf_token':  get_token(request),
        'MAX_FILE_UPLOAD_SIZE': settings.MAX_FILE_UPLOAD_SIZE,
        'MAX_NUMBER_OF_FILES': settings.MAX_NUMBER_OF_FILES
    }

    return render_to_response('downloader/upload.html', data, RequestContext(request))


def delete_uploaded(request, file_id):
    """
    Handle the deletion of the already uploaded file
    """
    if request.method == "DELETE":
        uploaded_file = get_object_or_404(UploadedFile, uuid=file_id)
        uploaded_file.delete()

        return HttpResponse(json.dumps(True))
    return HttpResponseBadRequest()


def data_upload(request):
    """
    Handle file upload
    """
    if request.method == "GET":
        #Return an empty list when plug-in requests a list of already uploaded files
        return HttpResponse("[]")

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            # let Ajax Upload know whether we saved it or not

            ret_json = [{"name": obj.filename, "size": obj.file.size, "delete_type":"DELETE", 'file_id': obj.uuid,
                        'delete_url': reverse("delete_uploaded", kwargs={'file_id': obj.uuid})}]
            return HttpResponse(json.dumps(ret_json))
        else:
            return HttpResponseBadRequest()

    return HttpResponseBadRequest()

