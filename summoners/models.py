from django.db import models

# Create your models here.
class Summoner(models.Model):
    name = models.CharField(max_length=255, blank=True)
    summonerId = models.CharField(max_length=255, blank=True, unique=True)
    summonerLevel = models.IntegerField(blank=True, null=True)
    highestAchievedSeasonTier = models.CharField(max_length=255, blank=True)
    rank = models.CharField(max_length=255, blank=True)
    profileIconId = models.CharField(max_length=255, blank=True)
    revisionDate = models.IntegerField(blank=True,null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

	class Meta:
		unique_together = (('name', 'summoner_id'),)


class SummonerSummaryStats(models.Model):
    summoner_id = models.IntegerField()
    playerStatSummaryType = models.CharField(max_length=255, blank=True)
    wins = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)
    totalChampionKills = models.IntegerField(blank=True, null=True)
    totalTurretsKilled = models.IntegerField(blank=True, null=True)
    totalMinionKills = models.IntegerField(blank=True, null=True)
    totalNeutralMinionsKilled = models.IntegerField(blank=True, null=True)
    totalAssists = models.IntegerField(blank=True, null=True)
    ranked = models.BooleanField(default=False)