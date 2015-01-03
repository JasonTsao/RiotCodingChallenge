import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from riot.utils import retrieveSummonerbyName
from models import Account


def login_func(request):
	rtn_dict = {"success": False, "msg": "", 'next':''}
	next = request.GET.get('next', False)
	username = request.POST.get('username', False)
	region = request.POST.get('region', 'na')


	if username:
		username = username.lower()
		response = retrieveSummonerbyName(region, username)
		if type(response) is dict:
			try:
				user = None
				if len(Account.objects.filter(username=username, summonerId=response[username]['id'])) < 1:
					user = User.objects.create_user(username=username,
													password='riotrules')
				else:
					account = Account.objects.get(username=username)
					user = account.user
				account, created = Account.objects.get_or_create(user=user, username=username, summonerId=response[username]['id'])

				account.profileIconId = response[username]['profileIconId']
				account.summonerLevel = response[username]['summonerLevel']
				account.revisionDate = response[username]['revisionDate']
				account.save()
				user = authenticate(username=account.username, password='riotrules')
				if user is not None:
					user.backend = 'django.contrib.auth.backends.ModelBackend'
					user.save()
					login(request, user)

					if next:
						rtn_dict['next'] = next
					rtn_dict['success'] = True
				else:
					print 'user is none!'
			except Exception as e:
				print 'Unable to get login: {0}'.format(e)
		else:
			print 'Username is not a real username'
			rtn_dict['msg'] = 'Username is not a real username'
	else:
		print 'No username provided'
		rtn_dict['msg'] = 'Username is not a real username'

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")