from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("riot.api",
			url(r"^summoner/search/([A-Za-z0-9_\.-]+)", "getSummonerByName"),
			url(r"^stats/(\d+)", "getStatsBySummonerId"),
			url(r"^match_history/([A-Za-z0-9_\.-]+)", "getMatchDataBySummonerName"),
)