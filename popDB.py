import json, os

path = os.path.dirname(__file__) + r"\data\matches\\"

matchColl = [match for match in os.listdir(path) if match.endswith('.json')]

matchData = []

#for match in matchColl:
#    matchData[json.loads(match)]

print(json.loads(matchColl[1]))
