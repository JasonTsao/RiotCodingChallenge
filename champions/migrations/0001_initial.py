# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Champion'
        db.create_table(u'champions_champion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('champion_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rankedPlayEnabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'champions', ['Champion'])

        # Adding model 'Spell'
        db.create_table(u'champions_spell', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('champion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['champions.Champion'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image_full', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image_sprite', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image_group', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'champions', ['Spell'])


    def backwards(self, orm):
        # Deleting model 'Champion'
        db.delete_table(u'champions_champion')

        # Deleting model 'Spell'
        db.delete_table(u'champions_spell')


    models = {
        u'champions.champion': {
            'Meta': {'object_name': 'Champion'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'champion_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rankedPlayEnabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'champions.spell': {
            'Meta': {'object_name': 'Spell'},
            'champion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['champions.Champion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_full': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image_group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image_sprite': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['champions']