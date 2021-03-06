from RiotCodingChallenge.settings import RIOT_KEY as api_key
from rediscli import r as R

import json
import urllib
import urllib2
import logging

RIOT_API_URL = 'https://na.api.pvp.net'

from django.forms.models import model_to_dict
from accounts.models import Account
from champions.models import Champion, Spell, GeneralSpell
from summoners.models import Summoner, SummonerSummaryStats, SummonerChampionStats
from static_data.models import Mastery, Rune

logger = logging.getLogger("django.request")


def pushToNOSQLHash(key, push_item):
	'''
		Store dictionary style data to redis to be used as cache layer
	'''
	r = R.r
	r.hmset(key, push_item)


def retrieveAPIData(api_url):
	'''
		Base function for making calls to Riot API
	'''
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


'''
	DIRECT CALLS TO RIOT API
'''


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

	if type(response) is dict:
		try:
			return_value = response['matches'][0]
		except:
			return_value = response
	else:
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


'''
	HELPER FUNCTIONS FOR FORMING MATCH DATA, HANDLES HEAVY LIFTING OF SYSTEM API CALLS
'''


def getAndStoreMasteries(region):
	'''
		Store every mastery that can be pulled from Riot API
	'''
	get_masteries_url = '{0}/api/lol/static-data/{1}/v1.2/mastery?masteryListData=ranks,tree&api_key={2}'.format(RIOT_API_URL, region, api_key)
	response = retrieveAPIData(get_masteries_url)

	r = R.r

	for mastery_type, mastery_list in response['tree'].items():
		for data in mastery_list:
			for item in data['masteryTreeItems']:
				if item:
					r_mastery_key = 'mastery.{0}.hash'.format(item['masteryId'])
					mastery, created = Mastery.objects.get_or_create(mastery_id=item['masteryId'], name=response['data'][str(item['masteryId'])]['name'], mastery_type=mastery_type, prereq=item['prereq'])
					pushToNOSQLHash(r_mastery_key, model_to_dict(mastery))
	return response


def getAndStoreRunes(region):
	'''
		Store every rune that can be pulled from Riot API
	'''
	is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble = False
	secondary_addition = 0
	secondary_effect_type = ''

	get_masteries_url = '{0}/api/lol/static-data/{1}/v1.2/rune?api_key={2}'.format(RIOT_API_URL, region, api_key)
	response = retrieveAPIData(get_masteries_url)

	r = R.r

	if type(response) is dict:
		for rune_id, rune_data in response['data'].items():
			#break rune up into it's value and it's name
			desc_array = rune_data['description'].split(' ')

			r_rune_key = 'rune.{0}.hash'.format(rune_id)

			#handle cases where a rune give you a % boost
			if desc_array[0].endswith('%'):
				addition = desc_array[0][1:-1]
				effect_type = ' '.join(desc_array[1:])
			#deal with the stupid greater mark of hybrid penetration case
			elif rune_data['name'] == 'Greater Mark of Hybrid Penetration':
				#split rune into two parts which then turns into the same problem as before
				desc_split_array = rune_data['description'].split('/')
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
				#parse out name and value
				addition = desc_array[0][1:]
				effect_type = ' '.join(desc_array[1:])

			#save run object to DB
			try:
				rune_obj = Rune.objects.get(rune_id=rune_id)
			except Exception as e:
				rune_obj = Rune(rune_id=rune_id, name=rune_data['name'], addition=addition, effect_type=effect_type, rune_type=rune_data['rune']['type'], tier=rune_data['rune']['tier'])
				
				if is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble:
					rune_obj.secondary_addition = secondary_addition
					rune_obj.secondary_effect_type = secondary_effect_type

				rune_obj.save()

			#cache rune objs to redis layer so we can hit our db less
			pushToNOSQLHash(r_rune_key, model_to_dict(rune_obj))
	return response


def getChampionName(championId, region):
	champion_name = ''

	r = R.r
	r_champion_name_key = 'champion.name.{0}.value'.format(championId)
	champion_name = r.get(r_champion_name_key)

	if not champion_name:
		try:
			champion_name = Champion.objects.get(champion_id=championId).name
		except:
			response = retrieveChampionDataById(region, championId)
			if type(response) is dict:
				champion = Champion(champion_id=championId, name=response['name'], title=response['title'])
				champion.save()
				champion_name = champion.name

		r.set(r_champion_name_key, champion_name)

	return champion_name


def getSummonerSpell(spellId, region):
	spell_key = ''

	r = R.r
	r_summoner_spell_key = 'summoner.spell.{0}.value'.format(spellId)
	spell_key = r.get(r_summoner_spell_key)

	if not spell_key:
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

		r.set(r_summoner_spell_key, spell_key)

	return spell_key


def getBasicSummonerData(summonerIdsArray, matchup_dict, region):
	summonerIds = ','.join(summonerIdsArray)
	basicSummonerStats = retrieveBasicStatsBySummonerId(region, summonerIds)

	#I realize running this forloop to fill it up isn't the most efficient way but since it'll always be only 
	#10 players I figure this time should be short

	#save summoner level since this is the only time we'll usually see it
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


def getSummonerMasteries(masteries_list, matchId, summonerId,region):
	'''
		get a formatted masteries string : offense/defenese/utility
	'''

	masteries = ''
	masteries_dict = {'Offense':0, 'Defense': 0, 'Utility':0}

	r = R.r
	r_summoner_masteries_key = 'match.{0}.summoner.{1}.masteries.hash'.format(matchId, summonerId)
	masteries = r.get(r_summoner_masteries_key)
	masteries = False

	if not masteries:
		for mastery in masteries_list:
			try:
				r_mastery_key = 'mastery.{0}.hash'.format(mastery['masteryId'])
				mastery_obj = r.hgetall(r_mastery_key)

				if mastery_obj:
					masteries_dict[mastery_obj['mastery_type']] += mastery['rank']
				else:
					mastery_obj = Mastery.objects.get(mastery_id=mastery['masteryId'])
					masteries_dict[mastery_obj.mastery_type] += mastery['rank']
			except Exception as e:
				print 'Unable to get mastery: {0}'.format(e)

		masteries = '/'.join(['%s' % (value) for (key, value) in masteries_dict.items()])

		#cache the information just saved to Relational DB
		r.set(r_summoner_masteries_key, masteries)

	return masteries


def getSummonerRunes(runes_list, matchId, summonerId, region):
	runes = {}
	is_the_stupid_greater_mark_of_hybrid_penetration_thats_giving_me_trouble = False
	secondary_addition = 0
	secondary_effect_type = ''

	#check redis cache layer first to see if data already exists for this summoners rune setup for this match
	r = R.r
	r_summoner_runes_key = 'match.{0}.summoner.{1}.runes.hash'.format(matchId, summonerId)
	runes = r.hgetall(r_summoner_runes_key)

	if not runes:
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

		#cache the information just saved to Relational DB
		pushToNOSQLHash(r_summoner_runes_key, runes)

 	return runes


def getSummonerNormalWins(summonerId, region):
	'''
		Get information about this summoners previous matches
			wins
			ranked_wins
			kills
			deaths
			assists
	'''
 	player_stats = {'wins':0, 'ranked_wins':0, 'wins_with_champion':0, 'kills':0.0, 'deaths':0.0, 'assists':0.0, 'kda':'n/a'}
 	r = R.r
	r_summoner_stats_key = 'summoner.{0}.stats.hash'.format(summonerId)
	
	try:
		summoner_games = SummonerSummaryStats.objects.filter(summoner_id=summonerId)

		if not summoner_games:
		 	summoner_games = []
		 	response = retrieveStatsBySummonerId(region, summonerId)

		 	if type(response) is dict:
				 for summary in response['playerStatSummaries']:
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
					 			
					 		summoner_summary.averageChampionsKilled = aggregated_stats.get('averageChampionsKilled', None)
					 		summoner_summary.averageNumDeaths = aggregated_stats.get('averageNumDeaths', None)
					 		summoner_summary.averageAssists = aggregated_stats.get('averageAssists', None)
					 			

					 	if summary['playerStatSummaryType'][:6] == 'Ranked':
					 		summoner_summary.ranked = True

					 	summoner_summary.save()
					 	summoner_games.append(summoner_summary)
					except Exception as e:
					 	print 'Unable to save new summoner summary: {0}'.format(e)

		else:
			player_stats = r.hgetall(r_summoner_stats_key)
			if not player_stats:
				player_stats = {'wins':0, 'ranked_wins':0, 'wins_with_champion':0, 'kills':0.0, 'deaths':0.0, 'assists':0.0, 'kda':'n/a'}
				num_games = len(summoner_games)
				for game in summoner_games:
					player_stats['wins'] += game.wins
					if game.ranked:
						player_stats['ranked_wins'] += game.wins
				pushToNOSQLHash(r_summoner_stats_key, player_stats)

	except Exception as e:
		print 'Error retreiving summoner normal stats: {0}'.format(e)

 	return player_stats


def getSummonerChampionStats(summonerId, region, championId):
	'''
		Get information for a summoner for a specific championg (in ranked games only)
	'''
	r = R.r
	r_summoner_champion_stats_key = 'summoner.{0}.champion.{1}.stats.hash'.format(summonerId, championId)
	ranked_player_stats = r.hgetall(r_summoner_champion_stats_key)

	if not ranked_player_stats:
	 	ranked_player_stats = {'wins':0, 'losses':0,'kills':0.0, 'deaths':0.0, 'assists':0.0, 'kda':'n/a', 'sessions_played': 0}
	 	champion_stats_obj = False

	 	try:
	 		champion_obj = Champion.objects.get(champion_id=championId)
		 	try:
		 		champion_stats_obj = SummonerChampionStats.objects.get(summoner_id=summonerId,champion=champion_obj)
		 	except Exception as e:
		 		response = retrieveRankedStatsBySummonerId(region, summonerId)
		 		if type(response) is dict:
					 champion_stats = response['champions']
					 for champion in champion_stats:
					 	if champion['id'] == championId:
					 		stats = champion['stats']
						 	num_games = stats['totalSessionsPlayed']
						 	champion_stats_obj = SummonerChampionStats(summoner_id=summonerId, champion=champion_obj)
						 	champion_stats_obj.wins = stats['totalSessionsWon']
						 	champion_stats_obj.losses = stats['totalSessionsLost']
						 	champion_stats_obj.sessionsPlayed = num_games
						 	champion_stats_obj.averageChampionsKilled = float(stats['totalChampionKills'])/num_games
						 	champion_stats_obj.averageNumDeaths = float(stats['totalDeathsPerSession'])/num_games
						 	champion_stats_obj.averageAssists = float(stats['totalAssists'])/num_games
						 	champion_stats_obj.save()
						 	break

			if champion_stats_obj:
				ranked_player_stats['wins'] = champion_stats_obj.wins
				ranked_player_stats['losses'] = champion_stats_obj.losses
				ranked_player_stats['sessions_played'] = champion_stats_obj.sessionsPlayed

				ranked_player_stats['kills'] = champion_stats_obj.averageChampionsKilled
				ranked_player_stats['deaths'] = champion_stats_obj.averageNumDeaths
				ranked_player_stats['assists'] = champion_stats_obj.averageAssists

				if ranked_player_stats['kills'] and ranked_player_stats['deaths'] and ranked_player_stats['kills']:
					kda = ["%.1f" % (ranked_player_stats['kills']), "%.1f" % (ranked_player_stats['deaths']), "%.1f" % (ranked_player_stats['assists'])]
					ranked_player_stats['kda'] = '/'.join(kda)

				pushToNOSQLHash(r_summoner_champion_stats_key, ranked_player_stats)
		except Exception as e:
			print 'Unable to pull summoner champion stats: {0}'.format(e)

 	return ranked_player_stats