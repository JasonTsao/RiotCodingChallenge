from RiotCodingChallenge.settings import RIOT_KEY as api_key
import json
import urllib
import urllib2
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from utils import *

from accounts.models import Account
from champions.models import Champion, Spell, GeneralSpell
from summoners.models import Summoner

TEST_SUMMONER_ID = '37490585'
TEST_SUMMONER_ID_2 = '19926474'

RIOT_API_URL = 'https://na.api.pvp.net'

logger = logging.getLogger("django.request")

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

def getBasicStatsBySummonerId(request, summonerIds):
	'''
		API call for getting a summoners basic stats by summoner ID from Riot API

		Input:
			summonerIds: summoner IDs to use to query 

		Output:
			json dict with basic summoner stats
	'''
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region and summonerIds:

		response = retrieveBasicStatsBySummonerId(region, summonerIds)

		if type(response) is dict:
			rtn_dict['response'] = response
		else:
			rtn_dict['msg'] = response
			rtn_dict['response'] = {}
	else:
		rtn_dict['msg'] = 'Malformed request url'
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


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
		summonerIdsArray = []
		summonerName = account.username

		if region and summonerName:
			response = retrieveSummonerbyName(region, summonerName)

			if type(response) is dict:
				summonerId = response[summonerName]['id']

				#Get most recent match
				matchHistory = retrieveMatchHistoryBySummonerId(region, summonerId)
				matchId = matchHistory['matchId']

				#Get more relevant data about the most recent match
				matchData = retrieveMatchDataByMatchId(region, matchId)
				rtn_dict['matchData'] = matchData

				#Create usable data for each participant in the match
				for participant in matchData['participants']:
					participant_dict = {}
					#Get Champion name
					champion_name = getChampionName(participant['championId'], region)

					participant_dict['player'] = matchData['participantIdentities'].pop(0)['player']
					#Get specific Summoner Data
					try:
						summoner = Summoner.objects.get(summonerId=participant_dict['player']['summonerId'])
						participant_dict['summonerLevel'] = summoner.summonerLevel
					except:
						#collect summonerIds we don't have info on so we can use 1 call to riot instead of multiple
						summonerIdsArray.append(str(participant_dict['player']['summonerId']))


					#Add Summoner Spells and Masteries to return dict
					participant_dict['spell1'] = getSummonerSpell(participant['spell1Id'], region)
					participant_dict['spell2'] = getSummonerSpell(participant['spell2Id'], region)
					participant_dict['masteries'] = getSummonerMasteries(participant['masteries'],region)
					participant_dict['runes'] = getSummonerRunes(participant['runes'],region)

					participant_dict['champion_name'] = champion_name
					participant_dict['id'] = participant['participantId']
					participant_dict['highestAchievedSeasonTier'] = participant['highestAchievedSeasonTier']

					#Add participant dict to return dict
					if participant['participantId'] < 6:
						matchup_dict['opponent'].append(participant_dict)
					else:
						matchup_dict['challenger'].append(participant_dict)

				#Save personal summoner data and put info into return dict
				if len(summonerIdsArray) > 0:
					matchup_dict = getBasicSummonerData(summonerIdsArray, matchup_dict, region)

				#rtn_dict['response'] = matchData
				rtn_dict['matchup'] = matchup_dict
	except Exception as e :
		print 'Unable to grab user data: {0}'.format(e)
		logger.info('Unable to grab user data: {0}'.format(e))

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


def getAndStoreAllMasteries(request):
	rtn_dict = {"success": False, "msg": ""}

	region = request.GET.get('region', 'na')

	if region:
		response = getAndStoreMasteries(region)

		rtn_dict['response'] = response

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")