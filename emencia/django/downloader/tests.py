"""Unit tests for emencia.django.downloader"""
import base64
import shutil
from django.test import TestCase
from django.core.files import File
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from emencia.django.downloader.models import Download

class DownloadsTest(TestCase):
    """
    Tests for emencia.django.downloader application
    """

    def tearDown(self):
        shutil.rmtree("tests/private")

    def test_create_download(self):
        """
        create some downloads
        """

        #self.assertRaises(IntegrityError, Download.objects.create)
        data = {'file' : File(open("tests/test.txt"), "test.txt")}
        download1 = Download.objects.create(**data)
        data = {'file' : File(open("tests/test.txt"), "test.txt"),
                'password' : 'mysecret'}
        download2 = Download.objects.create(**data)

        # test unique slug for same upload files
        self.assertNotEqual(download1.slug, download2.slug)

        # try with a specify slug
        data = {'file' : File(open("tests/test.txt"), "test.txt"),
                'slug' : 'my_slug_for_test_file'}
        download3 = Download.objects.create(**data)
        self.assertEqual(download3.slug, 'my_slug_for_test_file')

    def test_get_file(self):
        """
        test to get the files
        """

        data = {'file' : File(open("tests/test.txt"), "test.txt")}
        download1 = Download.objects.create(**data)
        data = {'file' : File(open("tests/test.txt"), "test.txt"),
                'password' : 'mysecret'}
        download2 = Download.objects.create(**data)
        response = self.client.get(reverse('get_file', args=[download1.slug]))
        self.assertContains(response, u'test\n')
        self.assertEquals(response['content-type'], 'text/plain')
        response = self.client.get(reverse('get_file', args=[download2.slug]))
        self.failUnlessEqual(response.status_code, 401)
        response = self.client.get(reverse('get_file', args=[download2.slug]),
                                   **{'HTTP_AUTHORIZATION': 'Basic %s' % base64.b64encode(":%s" % download2.password)})
        self.assertContains(response, u'test\n')
        self.assertEquals(response['content-type'], 'text/plain')
