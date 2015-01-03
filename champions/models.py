from django.db import models


class Champion(models.Model):
	champion_id = models.BigIntegerField(unique=True)
	name = models.CharField(max_length=255, blank=True)
	title = models.CharField(max_length=255, blank=True)
	rankedPlayEnabled = models.BooleanField(default=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name


class Spell(models.Model):
	champion = models.ForeignKey(Champion)
	name = models.CharField(max_length=255, blank=True)
	key = models.CharField(max_length=255, blank=True)
	image_full = models.CharField(max_length=255, blank=True)
	image_sprite = models.CharField(max_length=255, blank=True)
	image_group = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.name


class GeneralSpell(models.Model):
	spellId = models.IntegerField(unique=True)
	name = models.CharField(max_length=255, blank=True)
	summonerLevel = models.IntegerField(null=True,blank=True)
	description = models.TextField()
	key = models.CharField(max_length=255, blank=True)
	image_full = models.CharField(max_length=255, blank=True)
	image_sprite = models.CharField(max_length=255, blank=True)
	image_group = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.name