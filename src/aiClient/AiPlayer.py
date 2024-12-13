# passen
from nis import match

data = {
        "runId": "rab1daec42eee",
        "type": "or",
        "index": 2,
        "response": {
            "type": "option"
        }
    }

#plättchen platzieren
data = {
    "runId":"rab1daec42eee",
    "type":"space",
    "spaceId":"48"
}

#"""
# karte(n) mit name ziehen/kaufen
data = {
    "runId":"rab1daec42eee",
    "type":"card",
    "cards":[
        "Nuclear Zone",
        "Nitrite Reducing Bacteria"
    ]
}
#"""

#"""
# projektkarte ausspielen
data = {
    "runId":"rab1daec42eee",
    "type":"or",
    "index":0,
    "response":{
        "type":"projectCard",
        "card":"Nitrite Reducing Bacteria",
        "payment":{
            "heat":0,"megaCredits":11,"steel":0,"titanium":0,"plants":0,"microbes":0,"floaters":0,"lunaArchivesScience":0,"spireScience":0,"seeds":0,"auroraiData":0,"graphene":0,"kuiperAsteroids":0,"corruption":0
        }
    }
}
#"""

#"""
# perform action
data = {
    "runId":"rab1daec42eee",
    "type":"or",
    "index":0,
    "response":{
        "type":"card",
        "cards":[
            "Nitrite Reducing Bacteria"
        ]
    }
}
#"""

# select option
data = {
        "runId": "rab1daec42eee",
        "type": "or",
        "index": 0,
        "response": {
            "type": "option"
        }
    }

# passen
data = {
        "runId": "rab1daec42eee",
        "type": "or",
        "index": 2,
        "response": {
            "type": "option"
        }
    }

import http.client
import json

def create_game():
    settings = {
        "players": [
            {
                "name": "Yellow",
                "color": "yellow",
                "beginner": False,
                "handicap": 0,
                "first": False
            },
            {
                "name": "ki",
                "color": "red",
                "beginner": False,
                "handicap": 0,
                "first": False
            },
            {
                "name": "Green",
                "color": "green",
                "beginner": False,
                "handicap": 0,
                "first": False
            }
        ],
        "corporateEra": True,
        "prelude": False,
        "prelude2Expansion": False,
        "draftVariant": True,
        "showOtherPlayersVP": False,
        "venusNext": False,
        "colonies": False,
        "turmoil": False,
        "customCorporationsList": [],
        "customColoniesList": [],
        "customPreludes": [],
        "bannedCards": [],
        "includedCards": [],
        "board": "tharsis",
        "seed": 0.8999786486180988,
        "solarPhaseOption": False,
        "promoCardsOption": False,
        "communityCardsOption": False,
        "aresExtension": False,
        "politicalAgendasExtension": "Standard",
        "moonExpansion": False,
        "pathfindersExpansion": False,
        "undoOption": False,
        "showTimers": True,
        "fastModeOption": False,
        "removeNegativeGlobalEventsOption": False,
        "includeVenusMA": True,
        "includeFanMA": False,
        "modularMA": False,
        "startingCorporations": 2,
        "soloTR": False,
        "initialDraft": False,
        "preludeDraftVariant": True,
        "randomMA": "No randomization",
        "shuffleMapOption": False,
        "randomFirstPlayer": True,
        "requiresVenusTrackCompletion": False,
        "requiresMoonTrackCompletion": False,
        "moonStandardProjectVariant": False,
        "moonStandardProjectVariant1": False,
        "altVenusBoard": False,
        "escapeVelocityMode": False,
        "escapeVelocityBonusSeconds": 2,
        "twoCorpsVariant": False,
        "ceoExtension": False,
        "customCeos": [],
        "startingCeos": 3,
        "startingPreludes": 4,
        "starWarsExpansion": False,
        "underworldExpansion": False
    }
    json_body = json.dumps(settings)
    connection = http.client.HTTPConnection("localhost", 8080)
    connection.request("PUT", "/game", body=json_body)
    response = connection.getresponse()
    return json.loads(response.read().decode())

def send_request(json_body):
    connection = http.client.HTTPConnection("localhost", 8080)
    connection.request("POST", "/player/input?id=" + player_id, body=json_body)
    response = connection.getresponse()
    return json.loads(response.read().decode())

new_game = create_game()
player_id = ""
for player in new_game["players"]:
    if player["name"] == "ki":
        player_id = player["id"]


json_payload = json.dumps(data)
parsed = send_request(json_payload)


print(parsed)
print(parsed["runId"])
print(parsed["waitingFor"]["type"])
print(parsed["waitingFor"])

if parsed["waitingFor"]["type"] == "card":
    card_names = parsed["waitingFor"]["cards"]
    first_card = card_names[0]
    card_name = first_card["name"]
    buy_card = {
        "runId": parsed["runId"],
        "type": "card",
        "cards": [
            card_name
        ]
    }
    print("buy card " + card_name)
    res = send_request(buy_card)
    print(res)
#elif parsed["waitingFor"]["type"] == "or":