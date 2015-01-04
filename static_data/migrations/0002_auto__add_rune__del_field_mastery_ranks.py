# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rune'
        db.create_table(u'static_data_rune', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rune_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tier', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rune_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('effect_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('addition', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'static_data', ['Rune'])

        # Deleting field 'Mastery.ranks'
        db.delete_column(u'static_data_mastery', 'ranks')


    def backwards(self, orm):
        # Deleting model 'Rune'
        db.delete_table(u'static_data_rune')

        # Adding field 'Mastery.ranks'
        db.add_column(u'static_data_mastery', 'ranks',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'static_data.mastery': {
            'Meta': {'object_name': 'Mastery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mastery_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'mastery_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prereq': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'static_data.rune': {
            'Meta': {'object_name': 'Rune'},
            'addition': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'effect_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rune_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'rune_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['static_data']