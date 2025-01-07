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
        #print("too expensive, draw again")

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

    print("player " + player.name + " chose corporation (" + str(available_cash) + " MC)" + game["dealtCorporationCards"][corporation]["name"] + " and drew these cards: " + str(card_names_selection))

    buy_initial_cards_json = json.dumps(buy_initial_cards)
    res = send_player_input(buy_initial_cards_json, player.id)
    #print(res)
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

    if "options" not in waiting_for:
        print(waiting_for["title"])
        if "message" in waiting_for["title"]:
            if waiting_for["title"]["message"].startswith("Select space for"):
                available_spaces = waiting_for["spaces"]
                selected_space = random.choice(available_spaces)
                select_space_data = {
                    "runId": player.run_id,
                    "type": "space",
                    "spaceId": selected_space
                }
                res = send_player_input(json.dumps(select_space_data), player.id)
                print("Select space")
                return res
            elif waiting_for["title"]["message"].startswith("Select player to decrease"):
                selected_player = random.choice(waiting_for["players"])
                pass_data = {
                    "runId": player.run_id,
                    "type": "player",
                    "player": selected_player
                }
                print(waiting_for)
                print("selected player " + selected_player + " to decrease")
                res = send_player_input(json.dumps(pass_data), player.id)
                return res
            elif waiting_for["title"]["message"].startswith("Select how to pay") and waiting_for["title"]["message"].endswith("standard project"):
                print("Select how to pay for standard project not yet implemented")
                print(waiting_for)
                exit(-1)
            else:
                print("LOOK HERE options message not yet implemented")
                print(waiting_for)
                exit(-1)
        elif waiting_for["title"].startswith("Select space for"):
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Select space")
            return res
        elif waiting_for["title"].startswith("Select space reserved for ocean to place greenery tile"):
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Select space reserved for ocean to place greenery tile")
            return res
        elif waiting_for["title"].startswith("Select how to pay for award"):
            print("Select how to pay for award not yet implemented")
            print(waiting_for)
            exit(-1)
        elif waiting_for["title"] == "Select a space with a steel or titanium bonus":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected space with a steel or titanium bonus (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space adjacent to a city tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected space adjacent to a city tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select builder card to copy":
            available_cards = waiting_for["cards"]
            selected_card = random.choice(available_cards)
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": [selected_card["name"]]
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("Selected builder card to copy (" + selected_card["name"] + ")")
            return res
        elif waiting_for["title"] == "Select place next to no other tile for city":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected place next to no other tile for city (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select 1 card(s) to keep":
            available_cards = waiting_for["cards"]
            selected_card = random.choice(available_cards)
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": [selected_card["name"]]
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("Selected card to keep (" + selected_card["name"] + ")")
            return res
        elif waiting_for["title"] == "Select 2 card(s) to keep":
            available_cards = waiting_for["cards"]
            card_selection = random.sample(available_cards, k=2)
            card_names_selection = list(
                map(
                    lambda card: card["name"], card_selection))
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": card_names_selection
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("Selected cards to keep (" + str(card_names_selection) + ")")
            return res
        elif waiting_for["title"] == "Select space next to greenery for special tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected space next to greenery for special tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select a space with a steel or titanium bonus adjacent to one of your tiles":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected a space with a steel or titanium bonus adjacent to one of your tiles (" + str(
                select_space_data["spaceId"]) + ")")
            return res
        else:
            print("LOOK HERE options title not yet implemented")
            print(waiting_for)
            exit(-1)

    action_index = random.randint(0, len(waiting_for["options"]) - 1)
    which_option = waiting_for["options"][action_index]
    if which_option["title"] == "Pass for this generation":
        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("passed")
        res = send_player_input(json.dumps(pass_data), player.id)
        return res
    elif which_option["title"] == "Play project card":
        project_cards = game["cardsInHand"]
        random_card = random.choice(project_cards)
        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "projectCard",
                "card": random_card["name"],
                "payment": {
                    "heat":0,
                    "megaCredits": random_card["calculatedCost"],
                    "steel":0,
                    "titanium":0,
                    "plants":0,
                    "microbes":0,
                    "floaters":0,
                    "lunaArchivesScience":0,
                    "spireScience":0,
                    "seeds":0,
                    "auroraiData":0,
                    "graphene":0,
                    "kuiperAsteroids":0,
                    "corruption":0
                }
            }
        }
        res = send_player_input(json.dumps(pass_data), player.id)
        if "message" in res and res["message"].startswith("Unknown"):
            #print(project_cards)
            #print(random_card)
            #print("playing project card threw an error (" + res["message"] + ")")
            #print(pass_data)
            #exit(-1)
            # TODO most likely a wrong error message thrown because conditions are not met -> retry
            return turn(player)
        elif "message" in res and res["message"] == "You do not have that many resources to spend":
            print(res["message"])
            print("Card costs: " + str(random_card["calculatedCost"]))
            print(game["thisPlayer"])
            exit(-1)
        print("play project card")
        return res
    elif which_option["title"] == "Standard projects":
        selected_standard_project = which_option["cards"][random.randint(0, len(which_option["cards"]) - 1)]["name"]
        standard_project_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "card",
                "cards": [selected_standard_project]
            }
        }
        res = send_player_input(json.dumps(standard_project_data), player.id)
        print("standard project (" + selected_standard_project + ")")
        if "message" in res and res["message"].endswith("not available"):
            print("retry because buying standard project threw error (" + res["message"] + ")")
            # essentially a hacky retry
            return turn(player)
        return res
    elif which_option["title"] == "Sell patents":
        project_cards = game["cardsInHand"]
        card_selection = random.sample(project_cards, random.randint(1, len(project_cards)))
        card_names_selection = list(
            map(
                lambda card: card["name"], card_selection))

        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "card",
                "cards": card_names_selection
            }
        }
        res = send_player_input(json.dumps(pass_data), player.id)
        print("sell patents")
        print(res)
        return res
    elif which_option["title"] == "Select one option":
        print("options: " + json.dumps(which_option))
        place_tile_data = {
            "runId": "rab1daec42eee",
            "type": "space",
            "spaceId": "48"
        }
        res = send_player_input(json.dumps(place_tile_data), player.id)
        print(res)
        return res
    elif which_option["title"] == "End Turn":
        end_turn_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(end_turn_data), player.id)
        print("End turn")
        return res
    elif which_option["title"] == "Convert 8 heat into temperature":
        convert_heat_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(convert_heat_data), player.id)
        print("Convert heat into temperature")
        return res
    elif which_option["title"] == "Convert 8 plants into greenery":
        # maybe falscher name?!
        convert_plants_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(convert_plants_data), player.id)
        print("Convert plants into greenery")
        return res
    elif which_option["title"] == "Perform an action from a played card":
        perform_card_action_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(perform_card_action_data), player.id)
        print("Performing card action")
        if "message" in res and res["message"].startswith("Not a valid"):
            print(res["message"])
            print("problem in: Perform an action from a played card")
            print(waiting_for)
            exit(-1)
        return res
    elif which_option["title"] == "Do nothing":
        do_nothing_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Do nothing")
        res = send_player_input(json.dumps(do_nothing_data), player.id)
        return res
    elif which_option["title"] == "Claim a milestone":
        do_nothing_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Claim a milestone")
        res = send_player_input(json.dumps(do_nothing_data), player.id)
        if "message" in res:
            print(res["message"])
            print(which_option)
            print("problem in: Claim a milestone")
            exit(-1)
        return res
    elif which_option["title"] == "Skip removal":
        skip_removal_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Skipped removal")
        res = send_player_input(json.dumps(skip_removal_data), player.id)
        return res
    elif which_option["title"] == "Skip removing plants":
        skip_removal_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Skipped removing plants")
        res = send_player_input(json.dumps(skip_removal_data), player.id)
        return res
    elif which_option["title"] == "Increase your plant production 1 step":
        increase_plant_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Increased plant production 1 step")
        res = send_player_input(json.dumps(increase_plant_production_data), player.id)
        return res
    elif which_option["title"] == "Select a card to discard":
        available_cards = which_option["cards"]
        selected_card = random.choice(available_cards)

        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "card",
                "cards": [selected_card["name"]]
            }
        }
        res = send_player_input(json.dumps(pass_data), player.id)
        print("Selected a card to discard (" + selected_card["name"] + ")")
        print(res)
        return res
    elif which_option["title"] == "Add a science resource to this card":
        add_science_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Added a science resource to this card")
        res = send_player_input(json.dumps(add_science_data), player.id)
        return res
    elif which_option["title"] == "Do not remove resource":
        dont_remove_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Didnt remove resource")
        res = send_player_input(json.dumps(dont_remove_data), player.id)
        return res
    elif which_option["title"] == "Increase your energy production 2 steps":
        increase_energy_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_energy_production_data), player.id)
        return res
    elif "message" not in which_option["title"]:
        print("bdsg LOOK HERE: " + which_option["title"] + " is not yet implemented")
        print(game)
        print(which_option)
        exit(-1)
    elif which_option["title"]["message"].startswith("Take first action"):
        # the case for inventrix, ...
        take_action_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(take_action_data), player.id)
        print("Took first action")
        return res
    elif which_option["title"]["message"].startswith("Fund an award"):
        print(which_option)
        print("fund award")
        which_award = which_option["options"]
        random_award = random.randint(0, len(which_award) - 1)
        fund_award_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "or",
                "index": random_award,
                "response": {
                    "type": "option"
                }
            }
        }
        res = send_player_input(json.dumps(fund_award_data), player.id)
        return res
    elif which_option["title"]["message"].startswith("Take first action"):
        print(which_option)
        print("take first action: ")  # + dumped_waiting_for)
        print("not implemented qwefdnhg98")
        exit(0)
    elif which_option["title"]["message"].startswith("Convert") and which_option["title"]["message"].endswith("into greenery"):
        print(which_option)
        available_spaces = which_option["spaces"]
        selected_space = random.choice(available_spaces)
        select_space_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "spaceId": selected_space,
                "type": "space",
            }
        }
        res = send_player_input(json.dumps(select_space_data), player.id)
        print("Selected space to place greenery")
        return res
    elif which_option["title"]["message"].startswith("Remove"):
        remove_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("removed something: " + which_option["title"]["message"])
        res = send_player_input(json.dumps(remove_data), player.id)
        return res
    elif which_option["title"]["message"] == "Steal ${0} M€ from ${1}":
        steal_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(steal_data), player.id)
        print("stole megacredits: " + which_option["title"]["message"])
        return res
    else:
        print("LOOK HERE 1234 not implemented")
        print(which_option)
        exit(0)
'''
    exit(0)

    for action_index, option in enumerate(waiting_for["options"]):
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

    for action_index, option in enumerate(waiting_for["options"]):
        if option["title"] == "Pass for this generation":
            pass_data = {
                "runId": player.run_id,
                "type": "or",
                "index": action_index,
                "response": {
                    "type": "option"
                }
            }
            res = send_player_input(json.dumps(pass_data), player.id)
            print(res)
            print("phase: " + res["game"]["phase"])
'''

def draft(player):
    game = get_game(player.id)
    print("generation: " + str(game["game"]["generation"]))
    waiting_for = game["waitingFor"]
    card_selection = random.choice(waiting_for["cards"])["name"]
    draw_data = {
        "runId": player.run_id,
        "type": "card",
        "cards": [card_selection]
    }
    res = send_player_input(json.dumps(draw_data), player.id)
    print(res)
    print("phase: " + res["game"]["phase"])
    return res


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

    if "waitingFor" in res and "title" in res["waitingFor"] and "message" in res["waitingFor"]["title"]:
        if res["waitingFor"]["title"]["message"].startswith("Select how to spend"):
            print("select how to spend in research phase is not yet implemented")
            print(res["waitingFor"])
            exit(-1)

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




