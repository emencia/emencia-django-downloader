"""Models for emencia.django.downloader"""
import random
from datetime import datetime
try:
    from hashlib import md5
except ImportError:
    #Python 2.4 support
    from md5 import new as md5

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UploadedFile(models.Model):
    """
    Need a separate model for a file since it comes in a separate request over AJAX.
    So first the file gets uploaded and then we associate this file with the form containing email information
    """
    file = models.FileField(_('file'), upload_to=settings.MEDIA_ROOT)
    filename = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)


class Download(models.Model):
    """
    Download model
    """
    file = models.ForeignKey(UploadedFile, null=False)
    password = models.CharField(_('password'), max_length=50, blank=True)
    slug = models.SlugField(_('slug'), help_text=_('Used for the URLs'))
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    last_download = models.DateTimeField(_('last download'), blank=True, null=True)

    def __unicode__(self):
        return self.file.file.url

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')
        ordering = ('file',)

    def filename(self):
        return self.file.filename

    def save(self, *args, **kwargs):
        if self.slug == '':
            name = "%s%s%i" % (self.file.filename, datetime.utcnow(), random.randint(0, 100000))
            self.slug = md5(name).hexdigest()

        return super(Download, self).save(*args, **kwargs)



