from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("matches.views",
			url(r"^search", "searchForMatches"),
			url(r"^view", "matchPage"),
)