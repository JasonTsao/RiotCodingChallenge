from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login(request):
	return render_to_response("login.html", {}, context_instance=RequestContext(request))


@login_required
def matchPage(request):
	#matchId = request.GET.get('matchId', False)
	return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))

