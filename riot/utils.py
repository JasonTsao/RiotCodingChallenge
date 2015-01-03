from RiotCodingChallenge.settings import RIOT_KEY as api_key
import json
import urllib
import urllib2

RIOT_API_URL = 'https://na.api.pvp.net'


def retrieveAPIData(api_url):
	response = {}
	try:
		conn = urllib2.urlopen(api_url)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()
	except urllib2.HTTPError as error:
		print 'Error when requesting from Riot API: {0}'.format(error)
		response = 'Error when requesting from Riot API: {0}'.format(error)
	return response


def retrieveSummonerbyName(region, summonerNames):
	get_summoner_url = '{0}/api/lol/{1}/v1.4/summoner/by-name/{2}?api_key={3}'.format(RIOT_API_URL, region, summonerNames, api_key)
	response = retrieveAPIData(get_summoner_url)
	return response


def retrieveBasicStatsBySummonerId(region, summonerIds):
	get_basic_summoner_stats_url = '{0}/api/lol/{1}/v1.4/summoner/{2}?api_key={3}'.format(RIOT_API_URL, region, summonerIds, api_key)
	response = retrieveAPIData(get_basic_summoner_stats_url)
	return response

def retrieveStatsBySummonerId(region, summonerIds):
	get_summoner_stats_url = '{0}/api/lol/{1}/v1.3/stats/by-summoner/{2}/summary?api_key={3}'.format(RIOT_API_URL, region, summonerIds, api_key)
	response = retrieveAPIData(get_summoner_stats_url)
	return response


def retrieveMatchHistoryBySummonerId(region, summonerId):
	get_summoner_match_history_url = '{0}/api/lol/{1}/v2.2/matchhistory/{2}?api_key={3}&beginIndex=0&endIndex=1'.format(RIOT_API_URL, region, summonerId, api_key)
	response = retrieveAPIData(get_summoner_match_history_url)

	return_value = ''
	try:
		return_value = response['matches'][0]
	except:
		return_value = response
	return return_value


def retrieveMatchDataByMatchId(region, matchId):
	get_match_data_url = '{0}/api/lol/{1}/v2.2/match/{2}?api_key={3}'.format(RIOT_API_URL, region, matchId, api_key)
	response = retrieveAPIData(get_match_data_url)
	return response


def retrieveChampionDataById(region, champId):
	#get_champion_data_url = '{0}/api/lol/static-data/{1}/v1.2/champion/{2}?champData=all&api_key={3}'.format(RIOT_API_URL, region, champId, api_key)
	get_champion_data_url = '{0}/api/lol/static-data/{1}/v1.2/champion/{2}?champData=spells&api_key={3}'.format(RIOT_API_URL, region, champId, api_key)
	response = retrieveAPIData(get_champion_data_url)
	return response