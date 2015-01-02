from django.db import models

MATCH_MODES = (('CLASSIC', 'CLASSIC'), 
				  ('ODIN', 'ODIN'),
				  ('ARAM', 'ARAM'),
				  ('TUTORIAL', 'TUTORIAL'),
				  ('ONEFORALL', 'ONEFORALL'),
				  ('ASCENSION', 'ASCENSION'),
				  ('FIRSTBLOOD', 'FIRSTBLOOD'),
				  ('KINGPORO', 'KINGPORO'))

MATCH_TYPES = (('CUSTOM_GAME', 'CUSTOM_GAME'), 
				  ('MATCHED_GAME', 'MATCHED_GAME'),
				  ('TUTORIAL_GAME', 'TUTORIAL_GAME'))

QUEUE_TYPES = (('CUSTOM', 'CUSTOM'), 
				  ('NORMAL_5x5_BLIND', 'NORMAL_5x5_BLIND'),
				  ('RANKED_SOLO_5x5', 'RANKED_SOLO_5x5'),
				  ('RANKED_PREMADE_5x5', 'RANKED_PREMADE_5x5'),
				  ('BOT_5x5', 'BOT_5x5'),
				  ('NORMAL_3x3', 'NORMAL_3x3'),
				  ('RANKED_PREMADE_3x3', 'RANKED_PREMADE_3x3'),
				  ('NORMAL_5x5_DRAFT', 'NORMAL_5x5_DRAFT'),
				  ('ODIN_5x5_BLIND', 'ODIN_5x5_BLIND'),
				  ('ODIN_5x5_DRAFT', 'ODIN_5x5_DRAFT'),
				  ('BOT_ODIN_5x5', 'BOT_ODIN_5x5'),
				  ('BOT_5x5_INTRO', 'BOT_5x5_INTRO'),
				  ('BOT_5x5_BEGINNER', 'BOT_5x5_BEGINNER'),
				  ('BOT_5x5_INTERMEDIATE', 'BOT_5x5_INTERMEDIATE'),
				  ('RANKED_TEAM_3x3', 'RANKED_TEAM_3x3'))



class Match(models.Model):
	matchId = models.BigIntegerField(blank=True, null=True) 
	mapId = models.IntegerField(blank=True, null=True)
	matchCreation = models.BigIntegerField(blank=True, null=True)
	matchDuration = models.BigIntegerField(blank=True, null=True)
	matchMode = models.CharField(max_length=255, blank=True, choices=MATCH_MODES)
	matchType = models.CharField(max_length=255, blank=True, choices=MATCH_TYPES)
	platformId = models.CharField(max_length=255, blank=True)
	queueType = models.CharField(max_length=255, blank=True, choices=QUEUE_TYPES)
	region = models.CharField(max_length=255, blank=True)
	season = models.CharField(max_length=255, blank=True)