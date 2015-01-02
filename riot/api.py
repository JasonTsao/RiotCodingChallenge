from RiotCodingChallenge.settings import RIOT_KEY as api_key
import json
import urllib
import urllib2

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from utils import *

from accounts.models import Account
from champions.models import Champion, Spell

TEST_SUMMONER_ID = '37490585'
TEST_SUMMONER_ID_2 = '19926474'

RIOT_API_URL = 'https://na.api.pvp.net'


'''
	SUMMONER API CALLS
'''

def getSummonerByName(request, summonerNames):
	'''
		API call for getting a summoners ID and other data from Riot API

		Input:
			summonerNames: summoner name to use to query 

		Output:
			json dict with summoner data
	'''
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
	'''
		API call for getting a summoners stats by summoner ID from Riot API

		Input:
			summonerIds: summoner IDs to use to query 

		Output:
			json dict with summoner stats
	'''
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
	'''
		API call for getting a summoners Match Data from Riot API

		Input:
			summonerName: summoner name to use to query 

		Output:
			json dict with summoner match history
	'''
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
	'''
		API call for getting a summoners Match Data from Riot API

		Input:
			request: HTTP Request object containing logged in user to check current match data

		Output:
			formatted json dict to be dumped to frontend for displaying match data
	'''
	rtn_dict = {"success": False, "msg": ""}
	matchup_dict = {'challenger':[], 'opponent':[]}

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


				for participant in matchData['participants']:
					participant_dict = {}
					champion_name = False
					try:
						champion_name = Champion.objects.get(champion_id=participant['championId']).name

					except:
						response = retrieveChampionDataById(region, participant['championId'])
						if type(response) is dict:
							champion = Champion(champion_id=participant['championId'], name=response['name'], title=response['title'])
							champion.save()
							champion_name = champion.name
						else:
							rtn_dict['msg'] = response

					participant_dict['champion_name'] = champion_name
					participant_dict['id'] = participant['participantId']
					participant_dict['player'] = matchData['participantIdentities'].pop(0)['player']

					if participant['participantId'] < 6:
						matchup_dict['challenger'].append(participant_dict)
					else:
						matchup_dict['opponent'].append(participant_dict)

				#rtn_dict['response'] = matchData
				rtn_dict['matchup'] = matchup_dict
	except Exception as e :
		print 'Unable to grab user data: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")

'''
	STATIC DATA (champion, items, languages, masteries, realms, runes, summoner-spells)
'''

def getChampionDataById(request, championId):
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region and championId:
		response = retrieveChampionDataById(region, championId)

		if type(response) is dict:
			print response
		rtn_dict['response'] = response

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")