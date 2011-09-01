# -*- coding: utf-8 -*-
import uuid

from django import forms
from django.forms.widgets import Textarea
from django.utils.translation import ugettext as _
from models import Download, UploadedFile

class ShareForm(forms.ModelForm):
    """
    Form for a Download
    """
    file_id = forms.CharField(widget=forms.HiddenInput, required=True,
                              error_messages={'required': _('Please upload at least one file')})
    my_mail = forms.EmailField(label=_('Notify me'), required=False)
    notify1 = forms.EmailField(label=_('E-mail 1'), required=False)
    notify2 = forms.EmailField(label=_('E-mail 2'), required=False)
    notify3 = forms.EmailField(label=_('E-mail 3'), required=False)
    comment = forms.CharField(widget=Textarea, label=_('Add a comment'),
                              required=False)

    class Meta:
        model = Download
        exclude = ['last_download', 'creation', 'slug', 'file']

    def save(self):
        object = super(ShareForm, self).save(commit=False)
        object.file = UploadedFile.objects.get(uuid=self.cleaned_data['file_id'])
        object.save()
        return object

class UploadForm(forms.ModelForm):
    """
    Form for a file upload
    """
    file = forms.FileField(required=True)

    class Meta:
        model = UploadedFile
        exclude = ['filename', 'uuid']

    def save(self):
        object = super(UploadForm, self).save(commit=False)
        object.filename = self.cleaned_data['file'].name
        object.uuid = str(uuid.uuid4())
        object.save()
        return object

