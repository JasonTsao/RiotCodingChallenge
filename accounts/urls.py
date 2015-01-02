from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("accounts.views",
			url(r"^login", "login_func"),
)