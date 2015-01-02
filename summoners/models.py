from django.db import models

# Create your models here.
class Summoner(models.Model):
    username = models.CharField(max_length=255, blank=True)
    summonerId = models.CharField(max_length=255, blank=True)
    summonerLevel = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=255, blank=True)
    profileIconId = models.CharField(max_length=255, blank=True)
    revisionDate = models.IntegerField(blank=True,null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username

	class Meta:
		unique_together = (('username', 'summoner_id'),)