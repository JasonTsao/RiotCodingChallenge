# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rune.secondary_addition'
        db.add_column(u'static_data_rune', 'secondary_addition',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rune.secondary_addition'
        db.delete_column(u'static_data_rune', 'secondary_addition')


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
            'secondary_addition': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['static_data']