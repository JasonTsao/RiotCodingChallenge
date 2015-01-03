from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login(request):
	print 'at matches login!'
	print request.user
	if request.user.is_authenticated():
		print 'is user'
		return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))
	else:
		print 'needs to login'
		return render_to_response("login.html", {}, context_instance=RequestContext(request))


@login_required
def matchPage(request):
	if request.user.is_authenticated():
		#matchId = request.GET.get('matchId', False)
		return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))
	else:
		return render_to_response("login.html", {}, context_instance=RequestContext(request))
