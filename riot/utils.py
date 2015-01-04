from RiotCodingChallenge.settings import RIOT_KEY as api_key
import json
import urllib
import urllib2
import logging

RIOT_API_URL = 'https://na.api.pvp.net'

from accounts.models import Account
from champions.models import Champion, Spell, GeneralSpell
from summoners.models import Summoner, SummonerSummaryStats
from static_data.models import Mastery, Rune

logger = logging.getLogger("django.request")

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


def retrieveRankedStatsBySummonerId(region, summonerId):
	get_ranked_summoner_data_url = '{0}/api/lol/{1}/v1.3/stats/by-summoner/{2}/ranked?api_key={3}'.format(RIOT_API_URL, region, summonerId, api_key)
	response = retrieveAPIData(get_ranked_summoner_data_url)
	return response


def retrieveSpellDataById(region, spellId):
	get_summoner_stats_url = '{0}/api/lol/static-data/{1}/v1.2/summoner-spell/{2}?api_key={3}'.format(RIOT_API_URL, region, spellId, api_key)
	response = retrieveAPIData(get_summoner_stats_url)
	return response


def retrieveMatchHistoryBySummonerId(region, summonerId):
	get_summoner_match_history_url = '{0}/api/lol/{1}/v2.2/matchhistory/{2}?api_key={3}&beginIndex=0&endIndex=1'.format(RIOT_API_URL, region, summonerId, api_key)
	response = retrieveAPIData(get_summoner_match_history_url)

	return_value = ''
	try:
		return_value = response['matches'][0]
	except:
		print response
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


def retrieveRuneDataById(region, runeId):
	get_rune_data_url = '{0}/api/lol/static-data/{1}/v1.2/rune/{2}?&api_key={3}'.format(RIOT_API_URL, region, runeId, api_key)
	response = retrieveAPIData(get_rune_data_url)
	return response


def getAndStoreMasteries(region):
	get_masteries_url = '{0}/api/lol/static-data/{1}/v1.2/mastery?masteryListData=ranks,tree&api_key={2}'.format(RIOT_API_URL, region, api_key)
	response = retrieveAPIData(get_masteries_url)

	for mastery_type, mastery_list in response['tree'].items():
		for data in mastery_list:
			for item in data['masteryTreeItems']:
				if item:
					mastery = Mastery.objects.get_or_create(mastery_id=item['masteryId'], name=response['data'][str(item['masteryId'])]['name'], mastery_type=mastery_type, prereq=item['prereq'])
	return response


def getChampionName(championId, region):
	champion_name = ''
	try:
		champion_name = Champion.objects.get(champion_id=championId).name
	except:
		response = retrieveChampionDataById(region, championId)
		if type(response) is dict:
			champion = Champion(champion_id=championId, name=response['name'], title=response['title'])
			champion.save()
			champion_name = champion.name
	return champion_name

def getSummonerSpell(spellId, region):
	spell_key = ''
	try:
		spell = GeneralSpell.objects.get(spellId=spellId)
		spell_key = spell.key
	except:
		try:
			response = retrieveSpellDataById(region, spellId)
			spell = GeneralSpell(spellId=response['id'],name=response['name'], key=response['key'], description=response['description'],
								summonerLevel=response['summonerLevel'])
			spell.save()
			spell_key = spell.key
		except Exception as e:
			logger.info('Unable to get spell ID data: {0}'.format(e))

	return spell_key


def getBasicSummonerData(summonerIdsArray, matchup_dict, region):
	summonerIds = ','.join(summonerIdsArray)
	basicSummonerStats = retrieveBasicStatsBySummonerId(region, summonerIds)

	#I realize running this forloop to fill it up isn't the most efficient way but since it'll always be only 
	#10 players I figure this time should be short

	if type(basicSummonerStats) is dict:
		for k, v in basicSummonerStats.items():
			summoner = False
			for participant in matchup_dict['challenger']:
				if str(participant['player']['summonerId']) == str(k):
					participant['summonerLevel'] = v['summonerLevel']
					summoner = Summoner(name=v['name'].lower(), summonerId=v['id'], summonerLevel=v['summonerLevel'], profileIconId=v['profileIconId'], 
										revisionDate=v['revisionDate'], highestAchievedSeasonTier=participant['highestAchievedSeasonTier'])
					summoner.save()
					break

			if not summoner:
				for participant in matchup_dict['opponent']:
					if str(participant['player']['summonerId']) == str(k):
						participant['summonerLevel'] = v['summonerLevel']
						summoner = Summoner(name=v['name'].lower(), summonerId=v['id'], summonerLevel=v['summonerLevel'], profileIconId=v['profileIconId'], 
											revisionDate=v['revisionDate'], highestAchievedSeasonTier=participant['highestAchievedSeasonTier'])
						summoner.save()
						break
	else:
		print 'Unable to retreive basic summoner data'
	return matchup_dict


def getSummonerMasteries(masteries_list, region):

	masteries = ''
	masteries_dict = {'Offense':0, 'Defense': 0, 'Utility':0}

	for mastery in masteries_list:
		try:
			mastery_obj = Mastery.objects.get(mastery_id=mastery['masteryId'])
			masteries_dict[mastery_obj.mastery_type] += mastery['rank']
		except Exception as e:
			print 'Unable to get mastery: {0}'.format(e)

	masteries = '/'.join(['%s' % (value) for (key, value) in masteries_dict.items()])

	return masteries


def getSummonerRunes(runes_list, region):
	runes = {}
	is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble = False
	secondary_addition = 0
	secondary_effect_type = ''

	for rune in runes_list:
		try:
			rune_obj = Rune.objects.get(rune_id=rune['runeId'])
			try:
				runes[rune_obj.effect_type] += rune_obj.addition * rune['rank']
			except:
				runes[rune_obj.effect_type] = rune_obj.addition * rune['rank']

			if rune_obj.name == 'Greater Mark of Hybrid Penetration':
				try:
					runes[rune_obj.secondary_effect_type] += rune_obj.secondary_addition * rune['rank']
				except:
					runes[rune_obj.secondary_effect_type] = rune_obj.secondary_addition * rune['rank']
		except:
			response = retrieveRuneDataById(region, rune['runeId'])

			desc_array = response['description'].split(' ')

			if desc_array[0].endswith('%'):
				addition = desc_array[0][1:-1]
				effect_type = ' '.join(desc_array[1:])
			elif response['name'] == 'Greater Mark of Hybrid Penetration':
				desc_split_array = response['description'].split('/')
				desc_split_array[0] = desc_split_array[0].strip()
				desc_split_array[1] = desc_split_array[1].strip()

				first_array = desc_split_array[0].split(' ')
				second_array = desc_split_array[1].split(' ')

				addition = first_array[0][1:]
				effect_type = ' '.join(first_array[1:])

				secondary_addition = second_array[0][1:]
				secondary_effect_type = ' '.join(second_array[1:])

				is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble = True

			else:
				addition = desc_array[0][1:]
				effect_type = ' '.join(desc_array[1:])

			rune_obj = Rune(rune_id=rune['runeId'], name=response['name'], addition=addition, effect_type=effect_type, rune_type=response['rune']['type'], tier=response['rune']['tier'])
			
			if is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble:
				rune_obj.secondary_addition = secondary_addition
				rune_obj.secondary_effect_type = secondary_effect_type

			rune_obj.save()

			if is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble:
				runes[rune_obj.effect_type] = rune_obj.addition * rune['rank']
				runes[rune_obj.secondary_effect_type] = rune_obj.secondary_effect_type * rune['rank']
			else:
				runes[rune_obj.effect_type] = rune_obj.addition * rune['rank']

 	return runes


def getSummonerNormalWins(summonerId, region):
 	wins = 0

 	try:
 		#response = retrieveStatsBySummonerId(region, summonerId)
		#for summary in response['playerStatSummaries']:
		#	wins += summary.get('wins', 0)

	 	summoner_games = SummonerSummaryStats.objects.filter(summoner_id=summonerId)
	 	if len(summoner_games) > 0:
		 	for game in summoner_games:
		 		wins += game.wins

		else:
	 		response = retrieveStatsBySummonerId(region, summonerId)

	 		if type(response) is dict:
			 	for summary in response['playerStatSummaries']:
			 		wins += summary.get('wins', 0)
			 		try:
				 		summoner_summary = SummonerSummaryStats(summoner_id=summonerId,
				 												wins=summary.get('wins', None),
				 												losses=summary.get('losses', None), 
				 												playerStatSummaryType=summary.get('playerStatSummaryType', None))
				 		if summary['aggregatedStats']:
				 			aggregated_stats = summary['aggregatedStats']
				 			summoner_summary.totalChampionKills = aggregated_stats.get('totalChampionKills', None)
				 			summoner_summary.totalTurretsKilled = aggregated_stats.get('totalTurretsKilled', None)
				 			summoner_summary.totalMinionKills = aggregated_stats.get('totalMinionKills', None)
				 			summoner_summary.totalNeutralMinionsKilled = aggregated_stats.get('totalNeutralMinionsKilled', None)
				 			summoner_summary.totalAssists = aggregated_stats.get('totalAssists', None)

				 		summoner_summary.save()
				 	except Exception as e:
				 		print 'Unable to save new summoner summary: {0}'.format(e)
			else:
				print response


 	except Exception as e:
 		print 'Error retreiving summoner: {0}'.format(e)

 	return wins

def getSummonerRankedWins(summonerId, region):
 	pass