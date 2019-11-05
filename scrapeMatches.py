# Forrit sem sækir nýja leiki frá Riot API
# Þarf að setja nothæfan APIKey í breytuna (endast bara í 24 tíma)
# Einnig þarf að stilla date_time breytu, sækir leiki milli þessarar dagsetningar og dagsins í dag. Best að miða við dagsetningu á síðasta patch.
# Náum í síðustu 10 leiki sem einhver spilari spilaði (sniðugt að byrja á hátt rated spilara til að fá hágæða leiki), tökum gögn úr þeim og vistum sem json file
# Byrjunar ID sett í AvailableIds fylki
# Tökum einnig id á öðrum spilurum í leikjunum og notum þau til að finna næstu 10 leiki
# Hægt að stilla hversu lengi forrit vinnur með því að breyta Cycles breytu. Koma yfirleitt sirka 5 files per Cycle en fer eftir hversu hátt rankaður byrjunar ID accountinn er
# Run með python scrapeMatches.py eða scrapeMatches.py í cmd

# Kóði tekinn upprunalega frá https://github.com/davidweatherall/League-Data-Scraping-And-Analytics og breytt.

import urllib.request, json
import time



apiKey = ''

date_time = '24.10.2019 05:00:00'
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern))*1000)

UserId = 0
UsersDone = []
AvailableIds = ['yO7VTZRB4S-_CJZi1RJfi_9xlRrGm8TSVUmFwFF8tFUiZHs']
GamesDone = []
MatchesDone = 0
PeopleChecked = []
Cycles = 1000


i = 0

while i < Cycles:

	if UserId == 0:
		i_len = 0
		while i_len < len(AvailableIds):
			if AvailableIds[i_len] not in UsersDone:
				UserId = AvailableIds[i_len]
				print('setting UserId as {}'.format(UserId))
				i_len = len(AvailableIds)
			i_len += 1



	if UserId == 0:
		print('UserId 0, breaking')
		break

	UsersDone.append(UserId)

	print('-----')
	print('stage 1')
	print(i)
	print('-----')
	urlMatchHistory = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + str(UserId) + '?queue=420&beginTime=' + str(epoch) + '&endIndex=10&api_key=' + apiKey

	try:
		with urllib.request.urlopen(urlMatchHistory) as url:

			data = json.loads(url.read().decode())


		for match in data['matches']:
			if match['gameId'] not in GamesDone:

				gameId = match['gameId']
				GamesDone.append(gameId)
				urlString = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + str(gameId) + '?api_key=' + str(apiKey)
				
				try:
					with urllib.request.urlopen(urlString) as url:
						json_raw = url.read().decode()
					dataGame = json.loads(json_raw)

					MatchesDone +=1
					json_file = open('data/singleMatches/{}.json'.format(str(gameId)), 'wb')
					json_file.write(json_raw.encode('utf-8'))
					json_file.close

					for participantid in dataGame['participantIdentities']:

						accId = participantid['player']['accountId']

						if accId not in AvailableIds:
							AvailableIds.append(accId)

				except urllib.error.HTTPError as err:
					print(str(err))
					if(str(err) == 'HTTP Error 429: Too Many Requests'):
						print('sleeping 1')
						time.sleep(30)

	except urllib.error.HTTPError as err:
		print(str(err))
		if(str(err) == 'HTTP Error 429: Too Many Requests'):
			print('sleeping 2')
			time.sleep(60)

			i-=1

		if(err.code == 404):
			UserId = 0

	UserId = 0
	i+=1

print("Number of games saved: " + str(MatchesDone))