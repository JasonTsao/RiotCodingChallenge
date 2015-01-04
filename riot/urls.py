from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("riot.api",
			url(r"^summoner/search/([A-Za-z0-9_\.-]+)", "getSummonerByName"),
			url(r"^stats/(\d+)", "getStatsBySummonerId"),
			url(r"^stats/basic/(\d+)", "getBasicStatsBySummonerId"),
			url(r"^stats/ranked/(\d+)", "getRankedStatsBySummonerId"),
			url(r"^match_history/([A-Za-z0-9_\.-]+)", "getMatchDataBySummonerName"),
			url(r"^match_data", "getUserMatchData"),
			url(r"^champion/(\d+)", "getChampionDataById"),
			url(r"^masteries/get/all", "getAndStoreAllMasteries"),
)