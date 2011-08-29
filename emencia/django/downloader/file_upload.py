import json
import uuid
import os
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.conf import settings

from models import UploadedFile


def data_upload(request):
    if request.method == "POST":
        # the file is stored raw in the request
        if request.is_ajax():
            upload = request
            is_raw = True
            # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
            try:
                filename = request.GET['qqfile']
            except KeyError:
                return HttpResponseBadRequest("AJAX request not valid")
        # not an ajax upload, so it was the "basic" iframe version with submission via form
        else:
            is_raw = False
            if len(request.FILES) == 1:
                # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
                # ID based on a random number, so it cannot be guessed here in the code.
                # Rather than editing Ajax Upload to pass the ID in the querystring,
                # observer that each upload is a separate request,
                # so FILES should only have one entry.
                # Thus, we can just grab the first (and only) value in the dict.
                upload = request.FILES.values()[0]
            else:
                raise Http404("Bad Upload")
            filename = upload.name


        # ------------------------
        # process and save the file
        unique_filename = str(uuid.uuid4())
        filepath = os.path.join(settings.MEDIA_ROOT, unique_filename)
        
        success = get_contents(upload, filepath, is_raw)
        file = UploadedFile()
        
        file.file = filepath
        file.filename = filename
        file.uuid = unique_filename
        file.save()
        
        ret_json = {'success': success, 'file_id': file.uuid}

        # let Ajax Upload know whether we saved it or not
        return HttpResponse(json.dumps(ret_json))


def get_contents(request, filename, is_raw_data):
    '''
    is_raw_data: if True, uploaded is an HttpRequest object with the file being
            the raw post data
            if False, uploaded has been submitted via the basic form
            submission and is a regular Django UploadedFile in request.FILES
    '''
    try:
        from io import BufferedWriter, FileIO
        with BufferedWriter(FileIO(filename, "wb")) as dest:
            # if the "advanced" upload, read directly from the HTTP request
            # with the Django 1.3 functionality
            if is_raw_data:
                foo = request.read(1024)
                while foo:
                    dest.write(foo)
                    foo = request.read(1024)
            # if not raw, it was a form upload so read in the normal Django chunks fashion
            else:
                for c in request.chunks():
                    dest.write(c)
            return True
    except IOError:
        # could not open the file most likely
        return False, None


