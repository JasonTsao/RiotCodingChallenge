# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mastery'
        db.create_table(u'static_data_mastery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mastery_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ranks', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('mastery_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('prereq', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'static_data', ['Mastery'])


    def backwards(self, orm):
        # Deleting model 'Mastery'
        db.delete_table(u'static_data_mastery')


    models = {
        u'static_data.mastery': {
            'Meta': {'object_name': 'Mastery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mastery_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'mastery_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prereq': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ranks': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['static_data']