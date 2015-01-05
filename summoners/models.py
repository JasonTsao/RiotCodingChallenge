from django.db import models
from champions.models import Champion

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
    totalDeathsPerSession = models.IntegerField(blank=True, null=True)
    totalAssists = models.IntegerField(blank=True, null=True)
    totalTurretsKilled = models.IntegerField(blank=True, null=True)
    totalMinionKills = models.IntegerField(blank=True, null=True)
    totalNeutralMinionsKilled = models.IntegerField(blank=True, null=True)

    averageChampionsKilled = models.FloatField(blank=True, null=True) 
    averageNumDeaths = models.FloatField(blank=True, null=True) 
    averageAssists = models.FloatField(blank=True, null=True)
    ranked = models.BooleanField(default=False)

    def __unicode__(self):
        ranked = ''
        if self.ranked:
            ranked = 'Ranked'
        else:
            ranked = 'Unranked'
        return '{0} : {1} : {2}'.format(self.summoner_id, self.playerStatSummaryType, ranked)


class SummonerChampionStats(models.Model):
    champion = models.ForeignKey(Champion)
    summoner_id = models.IntegerField()

    wins = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)
    totalChampionKills = models.IntegerField(blank=True, null=True)
    totalDeathsPerSession = models.IntegerField(blank=True, null=True)
    totalAssists = models.IntegerField(blank=True, null=True)
    totalTurretsKilled = models.IntegerField(blank=True, null=True)
    totalMinionKills = models.IntegerField(blank=True, null=True)
    totalNeutralMinionsKilled = models.IntegerField(blank=True, null=True)

    sessionsPlayed = models.IntegerField(blank=True, null=True)

    averageChampionsKilled = models.FloatField(blank=True, null=True) 
    averageNumDeaths = models.FloatField(blank=True, null=True) 
    averageAssists = models.FloatField(blank=True, null=True)
    ranked = models.BooleanField(default=True)

    def __unicode__(self):
        return '{0} : {1}'.format(self.summoner_id, self.champion.name)

    class Meta:
        unique_together = (('champion', 'summoner_id'),)