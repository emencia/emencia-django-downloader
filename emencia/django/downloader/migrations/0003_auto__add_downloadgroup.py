# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DownloadGroup'
        db.create_table('downloader_downloadgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('downloader', ['DownloadGroup'])

        # Adding M2M table for field downloads on 'DownloadGroup'
        db.create_table('downloader_downloadgroup_downloads', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('downloadgroup', models.ForeignKey(orm['downloader.downloadgroup'], null=False)),
            ('download', models.ForeignKey(orm['downloader.download'], null=False))
        ))
        db.create_unique('downloader_downloadgroup_downloads', ['downloadgroup_id', 'download_id'])


    def backwards(self, orm):
        
        # Deleting model 'DownloadGroup'
        db.delete_table('downloader_downloadgroup')

        # Removing M2M table for field downloads on 'DownloadGroup'
        db.delete_table('downloader_downloadgroup_downloads')


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
        'downloader.downloadgroup': {
            'Meta': {'object_name': 'DownloadGroup'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['downloader.Download']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
