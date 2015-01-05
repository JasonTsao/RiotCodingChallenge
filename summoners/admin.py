from django.contrib import admin
from summoners.models import Summoner, SummonerSummaryStats, SummonerChampionStats

admin.site.register(Summoner)
admin.site.register(SummonerSummaryStats)
admin.site.register(SummonerChampionStats)