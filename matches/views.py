from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def searchForMatches(request):
	return render_to_response("matches/search_match.html", {}, context_instance=RequestContext(request))


def matchPage(request):
	matchId = request.GET.get('matchId', False)

	if matchId:
		return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))

	else:
		return render_to_response("matches/search_match.html", {}, context_instance=RequestContext(request))
