# passen
import random

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

# analog zu in "/new-game" auf "create game" zu klicken
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


def send_player_input(json_body, player_id):
    connection = http.client.HTTPConnection("localhost", 8080)
    connection.request("POST", "/player/input?id=" + player_id, body=json_body)
    response = connection.getresponse()
    return json.loads(response.read().decode())


class Player:
    game_age = 0
    undo_count = 0
    run_id = ""

    def __init__(self, color, id, name):
        self.color = color
        self.id = id
        self.name = name

# research phase
def initial_research_phase(player):
    game = get_game(player.id)
    player.run_id = game["runId"]
    corporation = random.randint(0,1)
    startingMegaCredits = {
        "CrediCor": 57,
        "EcoLine": 36,
        "Helion": 42,
        "Interplanetary Cinematics": 30,
        "Inventrix": 45,
        "Mining Guild": 30,
        "PhoboLog": 23,
        "Tharsis Republic": 40,
        "Thorgate": 48,
        "United Nations Mars Initiative": 40,
        "Saturn Systems": 42, # TODO gehört das dazu???
        "Teractor": 60,
    }
    corporation_name = game["dealtCorporationCards"][corporation]["name"]
    available_cash = startingMegaCredits[corporation_name]
    #card_selection = list()
    while True:
        card_selection = random.sample(game["dealtProjectCards"], random.randint(0, 10))
        card_cost = sum(map(lambda card: card["calculatedCost"], card_selection))
        if card_cost <= available_cash:
            break
        print("too expensive, draw again")

    card_names_selection = list(
        map(
            lambda card: card["name"], card_selection))

    buy_initial_cards = {
        "runId": player.run_id,
        "type": "initialCards",
        "responses": [
            {
                "type": "card",
                "cards": [corporation_name]
            }, {
                "type": "card",
                "cards": card_names_selection
            }]
    }

    print("player " + player.name + " chose corporation " + game["dealtCorporationCards"][corporation]["name"] + " and drew these cards: " + str(card_names_selection))

    buy_initial_cards_json = json.dumps(buy_initial_cards)
    res = send_player_input(buy_initial_cards_json, player.id)
    print(res)
    print("phase: " + res["game"]["phase"])
    player.game_age = res["game"]["gameAge"]
    player.undo_count = res["game"]["undoCount"]
    #is_waiting = waiting_for(player)
    #print(is_waiting)
    return res

def waiting_for(player):
    connection = http.client.HTTPConnection("localhost", 8080)
    connection.request("GET", "/api/waitingfor?id=" + player.id + "&gameAge=" + str(player.game_age) + "&undoCount=" + str(player.undo_count))
    response = connection.getresponse()
    return json.loads(response.read().decode())

def get_game(player_id):
    connection = http.client.HTTPConnection("localhost", 8080)
    connection.request("GET", "/api/player?id=" + player_id)
    response = connection.getresponse()
    return json.loads(response.read().decode())

def turn(player):
    print("turn of " + player.name)
    game = get_game(player.id)
    print("generation: " + str(game["game"]["generation"]))
    waiting_for = game["waitingFor"]
    dumped_waiting_for = json.dumps(waiting_for, indent=2)
    #print("waiting for options: " + dumped_waiting_for)

    index = random.randint(0, len(waiting_for["options"]) - 1)
    which_option = waiting_for["options"][index]
    if which_option["title"] == "Pass for this generation":
        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "option"
            }
        }
        print("passed")
        res = send_player_input(json.dumps(pass_data), player.id)
        return res
    elif which_option["title"] == "Play project card":
        print("play project card")
    elif which_option["title"] == "Standard projects":
        print("standard projects")
    elif which_option["title"] == "Sell patents":
        print("sell patents")
    elif which_option["title"] == "Select one option":
        print("options: " + json.dumps(which_option))
        place_tile_data = {
            "runId": "rab1daec42eee",
            "type": "space",
            "spaceId": "48"
        }
        res = send_player_input(json.dumps(place_tile_data), player.id)
        print(res)
    elif which_option["title"]["message"].startswith("Fund an award"):
        print("fund award")
    elif which_option["title"]["message"].startswith("Take first action"):
        print("take first action: ")  # + dumped_waiting_for)
    else:
        print("not implemented")
        exit(0)

    exit(0)

    for index, option in enumerate(waiting_for["options"]):
        if option["title"] == "Pass for this generation":
            print("pass option")
        elif option["title"] == "Play project card":
            print("play project card")
        elif option["title"] == "Standard projects":
            print("standard projects")
        elif option["title"] == "Sell patents":
            print("sell patents")
        elif option["title"] == "Select one option":
            print("options: " + json.dumps(option))
            continue
            place_tile_data = {
                "runId": "rab1daec42eee",
                "type": "space",
                "spaceId": "48"
            }
            res = send_player_input(json.dumps(place_tile_data), player.id)
            print(res)
        elif option["title"]["message"].startswith("Fund an award"):
            print("fund award")
        elif option["title"]["message"].startswith("Take first action"):
            print("take first action: ")# + dumped_waiting_for)
        else:
            try:
                print("remaining: " + json.dumps(option))
            except Exception as e:
                print("error: " + str(e) + ", " + dumped_waiting_for)
            exit(0)
    exit(0)

    for index, option in enumerate(waiting_for["options"]):
        if option["title"] == "Pass for this generation":
            pass_data = {
                "runId": player.run_id,
                "type": "or",
                "index": index,
                "response": {
                    "type": "option"
                }
            }
            res = send_player_input(json.dumps(pass_data), player.id)
            print(res)
            print("phase: " + res["game"]["phase"])


def draft(player):
    game = get_game(player.id)
    print("generation: " + str(game["game"]["generation"]))
    waiting_for = game["waitingFor"]
    card_selection = random.choice(waiting_for["cards"])["name"]
    draw_data = {
        "runId": player.run_id,
        "type": "card",
        "cards": [
            card_selection
            #waiting_for["cards"][which_card]["name"],
        ]
    }
    res = send_player_input(json.dumps(draw_data), player.id)
    print(res)
    print("phase: " + res["game"]["phase"])


def research_phase(player):
    game = get_game(player.id)
    print("generation: " + str(game["game"]["generation"]))
    card_selection = list(
        map(
            lambda card: card["name"], random.sample(game["waitingFor"]["cards"], random.randint(0, 4))))
    buy_cards_data = {
        "runId": player.run_id,
        "type": "card",
        "cards": card_selection
        #"cards": [game["waitingFor"]["cards"][0]["name"], game["waitingFor"]["cards"][1]["name"]]
    }
    res = send_player_input(json.dumps(buy_cards_data), player.id)
    # TODO could be too expensive
    print(res)
    return res


def generation(first_player, second_player, third_player):
    print("new generation:")

    turn(first_player)
    turn(second_player)
    turn(third_player)

    # order of the three is arbitrary
    draft(first_player)
    draft(second_player)
    draft(third_player)

    # order of the three is arbitrary
    draft(first_player)
    draft(second_player)
    draft(third_player)

    # order of the three is arbitrary
    draft(first_player)
    draft(second_player)
    draft(third_player)

    # order of the three is arbitrary
    research_phase(first_player)
    research_phase(second_player)
    research_phase(third_player)


def rotation():
    generation(player1, player2, player3)
    generation(player2, player3, player1)
    generation(player3, player1, player2)

if __name__ == '__main__':
    new_game = create_game()
    print(new_game)
    player1 = Player(new_game["players"][0]["color"], new_game["players"][0]["id"], new_game["players"][0]["name"])
    player2 = Player(new_game["players"][1]["color"], new_game["players"][1]["id"], new_game["players"][1]["name"])
    player3 = Player(new_game["players"][2]["color"], new_game["players"][2]["id"], new_game["players"][2]["name"])

    print("turn: " + new_game["activePlayer"])

    # order among these 3 is arbitrary
    initial_research_phase(player1)
    initial_research_phase(player2)
    initial_research_phase(player3)

    for _ in range(10):
        rotation()

    exit(0)




