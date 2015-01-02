from RiotCodingChallenge.settings import RIOT_KEY as api_key
import json
import urllib
import urllib2

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from utils import retrieveSummonerbyName, retrieveStatsBySummonerId, retrieveMatchHistoryBySummonerId, retrieveMatchDataByMatchId

from accounts.models import Account

TEST_SUMMONER_ID = '37490585'
TEST_SUMMONER_ID_2 = '19926474'

RIOT_API_URL = 'https://na.api.pvp.net'


'''
	SUMMONER API CALLS
'''

def getSummonerByName(request, summonerNames):
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region and summonerNames:
		response = retrieveSummonerbyName(region, summonerNames)

		if type(response) is dict:
			rtn_dict['response'] = response
		else:
			rtn_dict['msg'] = response
			rtn_dict['response'] = {}
	else:
		rtn_dict['msg'] = 'Malformed request url'
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


'''
	STATS API CALLS
'''

def getStatsBySummonerId(request, summonerIds):
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region and summonerIds:

		response = retrieveStatsBySummonerId(region, summonerIds)

		if type(response) is dict:
			rtn_dict['response'] = response
		else:
			rtn_dict['msg'] = response
			rtn_dict['response'] = {}
	else:
		rtn_dict['msg'] = 'Malformed request url'
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


'''
	RECENT GAMES BY SUMMONER ID API CALLS
'''


'''
	MATCH DATA API CALLS
'''

def getMatchDataBySummonerName(request, summonerName):
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region and summonerName:
		response = retrieveSummonerbyName(region, summonerName)

		if type(response) is dict:
			summonerId = response[summonerName]['id']
			matchHistory = retrieveMatchHistoryBySummonerId(region, summonerId)
			matchId = matchHistory['matchId']

			matchData = retrieveMatchDataByMatchId(region, matchId)
			rtn_dict['response'] = matchData

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")

@login_required
def getUserMatchData(request):
	rtn_dict = {"success": False, "msg": ""}

	try:
		account = Account.objects.get(user=request.user)
		#region = account.region
		region = 'na'
		summonerName = account.username

		if region and summonerName:
			response = retrieveSummonerbyName(region, summonerName)

			if type(response) is dict:
				summonerId = response[summonerName]['id']
				matchHistory = retrieveMatchHistoryBySummonerId(region, summonerId)
				matchId = matchHistory['matchId']

				matchData = retrieveMatchDataByMatchId(region, matchId)
				rtn_dict['response'] = matchData
	except Exception as e :
		print 'Unable to grab user data: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")

'''
	STATIC DATA (champion, items, languages, masteries, realms, runes, summoner-spells)
'''