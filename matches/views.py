from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login(request):
	if request.user.is_authenticated():
		return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))
	else:
		return render_to_response("login.html", {}, context_instance=RequestContext(request))



def matchPage(request):
	if request.user.is_authenticated():
		return render_to_response("matches/match.html", {}, context_instance=RequestContext(request))
	else:
		return redirect('matches.views.login')
