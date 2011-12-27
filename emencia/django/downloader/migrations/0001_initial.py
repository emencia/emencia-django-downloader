# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UploadedFile'
        db.create_table('downloader_uploadedfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('downloader', ['UploadedFile'])

        # Adding model 'Download'
        db.create_table('downloader_download', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['downloader.UploadedFile'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_download', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('downloader', ['Download'])


    def backwards(self, orm):
        
        # Deleting model 'UploadedFile'
        db.delete_table('downloader_uploadedfile')

        # Deleting model 'Download'
        db.delete_table('downloader_download')


    models = {
        'downloader.download': {
            'Meta': {'ordering': "('file',)", 'object_name': 'Download'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['downloader.UploadedFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_download': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'downloader.uploadedfile': {
            'Meta': {'object_name': 'UploadedFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['downloader']
