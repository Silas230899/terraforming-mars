import math
import random
import http.client
import json

http_connection = http.client.HTTPConnection("localhost", 8080)

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
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("PUT", "/game", body=json_body)
    response = http_connection.getresponse()
    return json.loads(response.read().decode())


def send_player_input(json_body, player_id):
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("POST", "/player/input?id=" + player_id, body=json_body)
    response = http_connection.getresponse()
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
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("GET", "/api/waitingfor?id=" + player.id + "&gameAge=" + str(player.game_age) + "&undoCount=" + str(player.undo_count))
    response = http_connection.getresponse()
    return json.loads(response.read().decode())

def get_game(player_id):
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("GET", "/api/player?id=" + player_id)
    response = http_connection.getresponse()
    return json.loads(response.read().decode())

def turn(player):
    print("turn of " + player.name)
    game = get_game(player.id)
    print("generation: " + str(game["game"]["generation"]))
    if "waitingFor" not in game:
        print("waiting for not in game warum auch immer")
        print(game)
        exit(-1)
    waiting_for = game["waitingFor"]

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
            elif waiting_for["title"]["message"].startswith("Select card to add"):
                available_cards = waiting_for["cards"]
                max = waiting_for["max"]
                min = waiting_for["min"]
                if min != 1 or max != 1:
                    print(waiting_for)
                    print("problem 024029sdbvfsbb5f48z")
                    exit(-1)

                sample = random.sample(available_cards, random.randint(min, max))
                card_names_selection = list(
                    map(
                        lambda card: card["name"], sample))
                select_card_data = {
                    "runId": player.run_id,
                    "type": "card",
                    "cards": card_names_selection
                }
                res = send_player_input(json.dumps(select_card_data), player.id)
                print("selected card to add resources" + str(card_names_selection))
                return res
            elif waiting_for["title"]["message"].startswith("Select how to pay for") and waiting_for["title"]["message"].endswith("standard project"):
                cost = waiting_for["amount"]
                available_heat = game["thisPlayer"]["heat"]
                pay_heat = cost
                pay_mc = 0
                if cost > available_heat:
                    pay_heat = available_heat
                    pay_mc = cost - pay_heat

                select_payment_data = {
                    "runId": player.run_id,
                    "type": "payment",
                    "payment": {
                        "heat": pay_heat,
                        "megaCredits": pay_mc,
                        "steel": 0,
                        "titanium": 0,
                        "plants": 0,
                        "microbes": 0,
                        "floaters": 0,
                        "lunaArchivesScience": 0,
                        "spireScience": 0,
                        "seeds": 0,
                        "auroraiData": 0,
                        "graphene": 0,
                        "kuiperAsteroids": 0,
                        "corruption": 0
                    }
                }
                res = send_player_input(json.dumps(select_payment_data), player.id)
                print("payed for standard project with heat/megacredits")
                return res
            elif waiting_for["title"]["message"].startswith("Select how to pay for") and waiting_for["title"]["message"].endswith("milestone"):
                cost = waiting_for["amount"]
                available_heat = game["thisPlayer"]["heat"]
                pay_heat = cost
                pay_mc = 0
                if cost > available_heat:
                    pay_heat = available_heat
                    pay_mc = cost - pay_heat

                select_payment_data = {
                    "runId": player.run_id,
                    "type": "payment",
                    "payment": {
                        "heat": pay_heat,
                        "megaCredits": pay_mc,
                        "steel": 0,
                        "titanium": 0,
                        "plants": 0,
                        "microbes": 0,
                        "floaters": 0,
                        "lunaArchivesScience": 0,
                        "spireScience": 0,
                        "seeds": 0,
                        "auroraiData": 0,
                        "graphene": 0,
                        "kuiperAsteroids": 0,
                        "corruption": 0
                    }
                }
                res = send_player_input(json.dumps(select_payment_data), player.id)
                print("payed for milestone with heat/megacredits")
                return res
            elif waiting_for["title"]["message"].startswith("Select how to spend") and waiting_for["title"]["message"].endswith("cards"):
                cost = waiting_for["amount"]
                available_heat = game["thisPlayer"]["heat"]
                pay_heat = cost
                pay_mc = 0
                if cost > available_heat:
                    pay_heat = available_heat
                    pay_mc = cost - pay_heat

                select_payment_data = {
                    "runId": player.run_id,
                    "type": "payment",
                    "payment": {
                        "heat": pay_heat,
                        "megaCredits": pay_mc,
                        "steel": 0,
                        "titanium": 0,
                        "plants": 0,
                        "microbes": 0,
                        "floaters": 0,
                        "lunaArchivesScience": 0,
                        "spireScience": 0,
                        "seeds": 0,
                        "auroraiData": 0,
                        "graphene": 0,
                        "kuiperAsteroids": 0,
                        "corruption": 0
                    }
                }
                res = send_player_input(json.dumps(select_payment_data), player.id)
                print("spent for card heat/megacredits")
                return res
            elif waiting_for["title"]["message"].startswith("Select how to pay for") and waiting_for["title"]["message"].endswith("action"):
                cost = waiting_for["amount"]

                can_pay_with_heat = waiting_for["paymentOptions"]["heat"]
                can_pay_with_titanium = waiting_for["paymentOptions"]["titanium"]
                can_pay_with_steel = waiting_for["paymentOptions"]["steel"]

                available_heat = game["thisPlayer"]["heat"]
                available_mc = game["thisPlayer"]["megaCredits"]
                available_steel = game["thisPlayer"]["steel"]
                steel_value = game["thisPlayer"]["steelValue"]
                available_titanium = game["thisPlayer"]["titanium"]
                titanium_value = game["thisPlayer"]["titaniumValue"]
                available_plants = game["thisPlayer"]["plants"]

                pay_mc = 0
                pay_heat = 0
                pay_steel = 0
                pay_titanium = 0

                if can_pay_with_heat:
                    pay_heat = cost
                    if cost > available_heat:
                        pay_heat = available_heat
                        pay_mc = cost - pay_heat
                elif can_pay_with_titanium:
                    necessary_titanium = math.ceil(cost / titanium_value)
                    pay_titanium = necessary_titanium
                    titanium_worth = available_titanium * titanium_value
                    if cost > titanium_worth:
                        pay_mc = cost - titanium_worth
                        pay_titanium = available_titanium
                elif can_pay_with_steel:
                    necessary_steel = math.ceil(cost / steel_value)
                    pay_steel = necessary_steel
                    steel_worth = available_steel * steel_value
                    if cost > steel_worth:
                        pay_mc = cost - steel_worth
                        pay_steel = available_steel
                else:
                    print("can pay something else VPÖva8wv98z6v")
                    exit(-1)

                select_payment_data = {
                    "runId": player.run_id,
                    "type": "payment",
                    "payment": {
                        "heat": pay_heat,
                        "megaCredits": pay_mc,
                        "steel": pay_steel,
                        "titanium": pay_titanium,
                        "plants": 0,
                        "microbes": 0,
                        "floaters": 0,
                        "lunaArchivesScience": 0,
                        "spireScience": 0,
                        "seeds": 0,
                        "auroraiData": 0,
                        "graphene": 0,
                        "kuiperAsteroids": 0,
                        "corruption": 0
                    }
                }

                print(str(cost) + "b56zn payed: " + str(json.dumps(select_payment_data)))
                res = send_player_input(json.dumps(select_payment_data), player.id)
                print("payed for action with heat/megacredits/steel/titanium")
                return res
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
            cost = waiting_for["amount"]

            can_pay_with_heat = waiting_for["paymentOptions"]["heat"]
            can_pay_with_titanium = waiting_for["paymentOptions"]["titanium"]
            can_pay_with_steel = waiting_for["paymentOptions"]["steel"]

            available_heat = game["thisPlayer"]["heat"]
            available_mc = game["thisPlayer"]["megaCredits"]
            available_steel = game["thisPlayer"]["steel"]
            steel_value = game["thisPlayer"]["steelValue"]
            available_titanium = game["thisPlayer"]["titanium"]
            titanium_value = game["thisPlayer"]["titaniumValue"]
            available_plants = game["thisPlayer"]["plants"]

            pay_mc = 0
            pay_heat = 0
            pay_steel = 0
            pay_titanium = 0

            if can_pay_with_heat:
                pay_heat = cost
                if cost > available_heat:
                    pay_heat = available_heat
                    pay_mc = cost - pay_heat
            elif can_pay_with_titanium:
                necessary_titanium = math.ceil(cost / titanium_value)
                pay_titanium = necessary_titanium
                titanium_worth = available_titanium * titanium_value
                if cost > titanium_worth:
                    pay_mc = cost - titanium_worth
                    pay_titanium = available_titanium
            elif can_pay_with_steel:
                necessary_steel = math.ceil(cost / steel_value)
                pay_steel = necessary_steel
                steel_worth = available_steel * steel_value
                if cost > steel_worth:
                    pay_mc = cost - steel_worth
                    pay_steel = available_steel
            else:
                print("can pay with something else vö03vv430vöv4aq2tbz")
                exit(-1)

            select_payment_data = {
                "runId": player.run_id,
                "type": "payment",
                "payment": {
                    "heat": pay_heat,
                    "megaCredits": pay_mc,
                    "steel": pay_steel,
                    "titanium": pay_titanium,
                    "plants": 0,
                    "microbes": 0,
                    "floaters": 0,
                    "lunaArchivesScience": 0,
                    "spireScience": 0,
                    "seeds": 0,
                    "auroraiData": 0,
                    "graphene": 0,
                    "kuiperAsteroids": 0,
                    "corruption": 0
                }
            }

            res = send_player_input(json.dumps(select_payment_data), player.id)
            print("payed for award project with heat/megacredits/steel/titanium")
            return res
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
        elif waiting_for["title"] == "Select space next to at least 2 other city tiles":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Select space next to at least 2 other city tiles (" + str(
                select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select a land space to place an ocean tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id)
            print("Selected a land space to place an ocean tile (" + str(
                select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select amount of heat production to decrease":
            max = waiting_for["max"]
            min = waiting_for["min"]
            decrease_amount = random.randint(min, max)
            select_decrease_amount_data = {
                "runId": player.run_id,
                "type": "amount",
                "amount": decrease_amount
            }
            res = send_player_input(json.dumps(select_decrease_amount_data), player.id)
            print("decreased heat production by " + str(decrease_amount))
            return res
        elif waiting_for["title"] == "Select amount of energy to spend":
            max = waiting_for["max"]
            min = waiting_for["min"]
            spend_amount = random.randint(min, max)
            select_spend_amount_data = {
                "runId": player.run_id,
                "type": "amount",
                "amount": spend_amount
            }
            res = send_player_input(json.dumps(select_spend_amount_data), player.id)
            print("spent amount of energy " + str(spend_amount))
            return res
        elif waiting_for["title"] == "Select card(s) to buy":
            available_cards = waiting_for["cards"]
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 0 or max != 1:
                print(waiting_for)
                print("problem 87wzv89w489v4ö09")
                exit(-1)

            sample = random.sample(available_cards, random.randint(min, max))
            card_names_selection = list(
                map(
                    lambda card: card["name"], sample))
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": card_names_selection
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("selected card to buy" + str(card_names_selection))
            return res
        elif waiting_for["title"] == "Select card to remove 1 Microbe(s)":
            available_cards = waiting_for["cards"]
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 1 or max != 1:
                print(waiting_for)
                print("problem vwn097v40wvap84ut")
                exit(-1)

            sample = random.sample(available_cards, random.randint(min, max))
            card_names_selection = list(
                map(
                    lambda card: card["name"], sample))
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": card_names_selection
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("selected card to remove microbe" + str(card_names_selection))
            return res
        elif waiting_for["title"] == "Select how to pay for action":
            cost = waiting_for["amount"]

            can_pay_with_heat = waiting_for["paymentOptions"]["heat"]
            can_pay_with_titanium = waiting_for["paymentOptions"]["titanium"]
            can_pay_with_steel = waiting_for["paymentOptions"]["steel"]

            available_heat = game["thisPlayer"]["heat"]
            available_mc = game["thisPlayer"]["megaCredits"]
            available_steel = game["thisPlayer"]["steel"]
            steel_value = game["thisPlayer"]["steelValue"]
            available_titanium = game["thisPlayer"]["titanium"]
            titanium_value = game["thisPlayer"]["titaniumValue"]
            available_plants = game["thisPlayer"]["plants"]

            available_payments = ["mc"]
            if can_pay_with_heat:
                available_payments.append("heat")
            if can_pay_with_steel:
                available_payments.append("steel")
            if can_pay_with_titanium:
                available_payments.append("titanium")

            # generate order
            random.shuffle(available_payments)

            pay_mc = 0
            pay_heat = 0
            pay_steel = 0
            pay_titanium = 0


            if can_pay_with_heat:
                pay_heat = cost
                if cost > available_heat:
                    pay_heat = available_heat
                    pay_mc = cost - pay_heat

            if can_pay_with_titanium:
                necessary_titanium = math.ceil(cost / titanium_value)
                pay_titanium = necessary_titanium
                titanium_worth = available_titanium * titanium_value
                if cost > titanium_worth:
                    pay_mc = cost - titanium_worth
                    pay_titanium = available_titanium

            if can_pay_with_steel:
                necessary_steel = math.ceil(cost / steel_value)
                pay_steel = necessary_steel
                steel_worth = available_steel * steel_value
                if cost > steel_worth:
                    pay_mc = cost - steel_worth
                    pay_steel = available_steel

            select_payment_data = {
                "runId": player.run_id,
                "type": "payment",
                "payment": {
                    "heat": pay_heat,
                    "megaCredits": pay_mc,
                    "steel": pay_steel,
                    "titanium": pay_titanium,
                    "plants": 0,
                    "microbes": 0,
                    "floaters": 0,
                    "lunaArchivesScience": 0,
                    "spireScience": 0,
                    "seeds": 0,
                    "auroraiData": 0,
                    "graphene": 0,
                    "kuiperAsteroids": 0,
                    "corruption": 0
                }
            }

            print(str(cost) + " o8om8m payed: " + str(json.dumps(select_payment_data)))
            res = send_player_input(json.dumps(select_payment_data), player.id)
            print("payed for action with heat or titanium or steel")
            return res
        elif waiting_for["title"] == "Select how to pay for milestone":
            cost = waiting_for["amount"]
            available_heat = game["thisPlayer"]["heat"]
            pay_heat = cost
            pay_mc = 0
            if cost > available_heat:
                pay_heat = available_heat
                pay_mc = cost - pay_heat

            select_payment_data = {
                "runId": player.run_id,
                "type": "payment",
                "payment": {
                    "heat": pay_heat,
                    "megaCredits": pay_mc,
                    "steel": 0,
                    "titanium": 0,
                    "plants": 0,
                    "microbes": 0,
                    "floaters": 0,
                    "lunaArchivesScience": 0,
                    "spireScience": 0,
                    "seeds": 0,
                    "auroraiData": 0,
                    "graphene": 0,
                    "kuiperAsteroids": 0,
                    "corruption": 0
                }
            }
            res = send_player_input(json.dumps(select_payment_data), player.id)
            print("payed for milestone with heat/megacredits")
            return res
        elif waiting_for["title"] == "You cannot afford any cards":
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 0 or max != 0:
                print(waiting_for)
                print("problem z09z0<9zf0szfe09zs")
                exit(-1)

            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": []
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("couldnt afford any cards")
            return res
        elif waiting_for["title"] == "Select card to remove 1 Animal(s)":
            available_cards = waiting_for["cards"]
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 1 or max != 1:
                print(waiting_for)
                print("problem qc2qce8q98ezqzqceq2")
                exit(-1)

            sample = random.sample(available_cards, random.randint(min, max))
            card_names_selection = list(
                map(
                    lambda card: card["name"], sample))
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": card_names_selection
            }
            res = send_player_input(json.dumps(select_card_data), player.id)
            print("selected card to remove 1 animal from" + str(card_names_selection))
            return res
        else:
            print("LOOK HERE options title not yet implemented")
            print(waiting_for)
            exit(-1)
    #else:
        #options is in waiting for


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
        availableHeat = game["thisPlayer"]["heat"]
        availableMC = game["thisPlayer"]["megaCredits"]
        availableSteel = game["thisPlayer"]["steel"]
        steelValue = game["thisPlayer"]["steelValue"]
        availableTitanium = game["thisPlayer"]["titanium"]
        titaniumValue = game["thisPlayer"]["titaniumValue"]
        availablePlants = game["thisPlayer"]["plants"]

        #project_cards = game["cardsInHand"]
        playable_cards = which_option["cards"]
        random_card = random.choice(playable_cards)
        card_costs = random_card["calculatedCost"]

        use_heat = 0
        use_MC = 0
        use_steel = 0
        use_titanium = 0
        use_plants = 0
        if card_costs > availableMC:
            use_MC = availableMC
            remaining_card_costs = card_costs - availableMC
            necessary_steel = math.ceil(remaining_card_costs/steelValue)
            if necessary_steel > availableSteel:
                # TODO check if anything but mc is ever used
                use_steel = availableSteel
                remaining_card_costs -= availableSteel * steelValue
                necessary_titanium = math.ceil(remaining_card_costs/titaniumValue)
                if necessary_titanium > availableTitanium:
                    use_titanium = availableTitanium
                    if availableMC + availableSteel * steelValue + availableTitanium * titaniumValue > card_costs:
                       print("grad so gerettet")
                    else:
                        print("max av:" + str(availableMC + availableSteel * steelValue + availableTitanium * titaniumValue))
                        print("card" + random_card["name"])
                        print("cost: " + str(card_costs))
                        print(game["thisPlayer"])
                        print("not enough mc nor steel nor titanium a93uhjr")
                        # will trigger a retry
                        #exit(-1)
                else:
                    use_titanium = necessary_titanium
            else:
                use_steel = necessary_steel
        else:
            use_MC = card_costs

        can_pay_steel = False
        if "AI Central,Aquifer Pumping,Artificial Lake,Biomass Combustors,Building Industries,Capital,Carbonate Processing,Colonizer Training Camp,Commercial District,Corporate Stronghold,Cupola City,Deep Well Heating,Development Center,Domed Crater,Electro Catapult,Eos Chasma National Park,Equatorial Magnetizer,Food Factory,Fueled Generators,Fuel Factory,Fusion Power,Geothermal Power,GHG Factories,Great Dam,Greenhouses,Heat Trappers,Immigrant City,Industrial Center,Industrial Microbes,Ironworks,Magnetic Field Dome,Magnetic Field Generators,Mars University,Martian Rails,Medical Lab,Mine,Mining Area,Mining Rights,Mining Rights,Mining Rights,Mohole Area,Natural Preserve,Noctis City,Noctis Farming,Nuclear Power,Olympus Conference,Open City,Ore Processor,Peroxide Power,Physics Complex,Power Infrastructure,Power Plant,,Protected Valley,Rad-Chem Factory,Research Outpost,Rover Construction,Soil Factory,Solar Power,Space Elevator,Steelworks,Strip Mine,Tectonic Stress Power,Titanium Mine,Tropical Resort,Underground City,Underground Detonations,Urbanized Area,Water Splitting Plant,Windmills".find(
                random_card["name"]) != -1:
            can_pay_steel = True

        can_pay_titanium = False
        if "Space Elevator,Aerobraked Ammonia Asteroid,Asteroid,Asteroid Mining,Beam From A Thorium Asteroid,Big Asteroid,Callisto Penal Mines,Comet,Convoy From Europa,Deimos Down,Ganymede Colony,Giant Ice Asteroid,Giant Space Mirror,Ice Asteroid,Immigration Shuttles,Imported GHG,Imported Hydrogen,Imported Nitrogen,Import of Advanced GHG,Interstellar Colony Ship,Io Mining Industries,Lagrange Observatory,Large Convoy,Methane From Titan,Miranda Resort,Nitrogen-Rich Asteroid,Optimal Aerobraking,Phobos Space Haven,Satellites,Security Fleet,Shuttles,Solar Wind Power,Soletta,Space Mirrors,Space Station,Technology Demonstration,Terraforming Ganymede,Toll Station,Towing A Comet,Trans-Neptune Probe,Vesta Shipyard,Water Import From Europa".find(
                random_card["name"]) != -1:
            can_pay_titanium = True

        payment_options = which_option["paymentOptions"]
        can_pay_heat = payment_options["heat"]

        use_heat = 0
        use_MC = 0
        use_steel = 0
        use_titanium = 0
        use_plants = 0

        remaining = card_costs
        if availableMC >= remaining:
            use_MC = remaining
            remaining = 0
        else:
            use_MC = availableMC
            remaining = remaining - use_MC

        if can_pay_heat:
            if availableHeat >= remaining:
                use_heat = remaining
                remaining = 0
            else:
                use_heat = availableHeat
                remaining = remaining - use_heat

        if can_pay_steel:
            if availableSteel >= remaining:
                use_steel = remaining
                remaining = 0
            else:
                use_steel = availableSteel
                remaining = remaining - use_steel

        if can_pay_titanium:
            if availableTitanium >= remaining:
                use_titanium = remaining
                remaining = 0
            else:
                use_titanium = availableTitanium
                remaining = remaining - use_titanium

        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "projectCard",
                "card": random_card["name"],
                "payment": {
                    "heat":use_heat,
                    "megaCredits": use_MC,
                    "steel":use_steel,
                    "titanium":use_titanium,
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
            print(game)
            print(res)
            print(playable_cards)
            print(random_card)
            print("playing project card threw an error (" + res["message"] + ")")
            print(pass_data)
            print(payment_options)
            print("available mc: " + str(availableMC))
            exit(-1)
            # TODO most likely a wrong error message thrown because conditions are not met -> retry
            return turn(player)
        elif "message" in res and res["message"] == "You do not have that many resources to spend":
            print(res["message"])
            print("Card costs: " + str(random_card["calculatedCost"]))
            print(game["thisPlayer"])
            print(payment_options)
            print("available mc: " + str(availableMC))
            exit(-1)
        elif "message" in res and res["message"].startswith("Did not spend enough to pay for card"):
            # TODO when a card is selected the player cannot afford
            # has to be done another way but for now just retry
            print(game)
            print(res)
            print(playable_cards)
            print(random_card)
            print("playing project card threw an error (" + res["message"] + ")")
            print(pass_data)
            print(payment_options)
            print("available mc: " + str(availableMC))
            exit(-1)
            return turn(player)
        elif "message" in res and str(res["message"]).find("units of") != -1 and str(res["message"]).find("must be reserved for"): # such as "0 units of steel must be reserved for Security Fleet"
            # maybe an error idk
            print(game)
            print(res)
            print(playable_cards)
            print(random_card)
            print("playing project card threw an error (" + res["message"] + ")")
            print(pass_data)
            print(payment_options)
            print("available mc: " + str(availableMC))
            exit(-1)
            return turn(player)
        elif "message" in res:
            print("other message juhf984zt9e8th9e84t: " + res["message"])
            print(game["thisPlayer"])
            print(payment_options)
            print("available mc: " + str(availableMC))
            exit(-1)
        print("play project card")
        return res
    elif which_option["title"] == "Standard projects":
        # TODO only select standard project if resources are available
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
        #perform_card_action_data = {
        #    "runId": player.run_id,
        #    "type": "or",
        #    "index": action_index,
        #    "response": {
        #        "type": "option"
        #    }
        #}

        which_card = random.choice(which_option["cards"])["name"]
        perform_card_action_data = {
           "runId": player.run_id,
           "type": "or",
           "index": action_index,
            "response": {
                "type": "card",
                "cards": [which_card]
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
        available_milestones = which_option["options"]
        which_milestone = random.randint(0, len(available_milestones) - 1)
        claim_milestone_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "or",
                "index": which_milestone,
                "response": {
                    "type": "option"
                }
            }
        }
        print("Claim a milestone")
        res = send_player_input(json.dumps(claim_milestone_data), player.id)
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
    elif which_option["title"] == "Do not steal":
        dont_steal_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Didn't steal")
        res = send_player_input(json.dumps(dont_steal_data), player.id)
        return res
    elif which_option["title"] == "Remove 2 microbes to raise oxygen level 1 step":
        remove_microbes_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Removed 2 microbes to raise oxygen level 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id)
        return res
    elif which_option["title"] == "Add 1 microbe to this card":
        add_microbe_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Added 1 microbe to this card")
        res = send_player_input(json.dumps(add_microbe_data), player.id)
        return res
    elif which_option["title"] == "Remove 3 microbes to increase your terraform rating 1 step":
        remove_microbes_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Removed 3 microbes to increase your terraform rating 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id)
        return res
    elif which_option["title"] == "Select space for greenery tile":
        available_spaces = which_option["spaces"]
        selected_space = random.choice(available_spaces)
        select_space_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "space",
                "spaceId": selected_space
            }
        }
        res = send_player_input(json.dumps(select_space_data), player.id)
        print("Selected space to place greenery (" + selected_space + ")")
        return res
    elif which_option["title"] == "Don't place a greenery":
        dont_place_greenery_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Didnt place a greenery")
        res = send_player_input(json.dumps(dont_place_greenery_data), player.id)
        return res
    elif which_option["title"] == "Remove a science resource from this card to draw a card":
        remove_science_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Removed a science resource from this card to draw a card")
        res = send_player_input(json.dumps(remove_science_data), player.id)
        return res
    elif which_option["title"] == "Spend 1 steel to gain 7 M€.":
        spend_steel_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Spent 1 steel to gain 7 M€")
        res = send_player_input(json.dumps(spend_steel_data), player.id)
        return res
    elif which_option["title"] == "Remove 2 microbes to raise temperature 1 step":
        remove_microbes_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Removed 2 microbes to raise temperature 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id)
        return res
    elif which_option["title"] == "Add 3 microbes to a card":
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
        print("Added 3 microbes to a card (" + selected_card["name"] + ")")
        print(res)
        return res
    elif which_option["title"] == "Select card to add 2 microbes":
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
        print("Added 2 microbes to a card (" + selected_card["name"] + ")")
        print(res)
        return res
    elif which_option["title"] == "Select card to remove 2 Animal(s)":
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
        print("Removed 2 animals from card (" + selected_card["name"] + ")")
        print(res)
        return res
    elif which_option["title"] == "Select card to add 2 animals":
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
        print("Selected card to add 2 animals (" + selected_card["name"] + ")")
        print(res)
        return res
    elif which_option["title"] == "Gain 4 plants":
        gain_4_plants_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Gained 4 plants")
        res = send_player_input(json.dumps(gain_4_plants_data), player.id)
        return res
    elif which_option["title"] == "Spend 1 plant to gain 7 M€.":
        spent_plant_for_mc_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Spent 1 plant to gain 7 M€")
        res = send_player_input(json.dumps(spent_plant_for_mc_data), player.id)
        return res
    elif which_option["title"] == "Gain plant":
        gain_plant_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Gained plant")
        res = send_player_input(json.dumps(gain_plant_data), player.id)
        return res
    elif which_option["title"] == "Gain 1 plant":
        gain_1_plant_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Gained 1 plant")
        res = send_player_input(json.dumps(gain_1_plant_data), player.id)
        return res
    elif which_option["title"] == "Gain 3 plants":
        gain_3_plants_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Gained 3 plant")
        res = send_player_input(json.dumps(gain_3_plants_data), player.id)
        return res
    elif which_option["title"] == "Gain 5 plants":
        gain_5_plants_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Gained 5 plants")
        res = send_player_input(json.dumps(gain_5_plants_data), player.id)
        return res
    elif which_option["title"] == "Don't remove M€ from adjacent player":
        dont_remove_mc_from_adjacent_player_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        print("Didnt remove mc from adjacent player")
        res = send_player_input(json.dumps(dont_remove_mc_from_adjacent_player_data), player.id)
        return res
    elif which_option["title"] == "Select adjacent player to remove 4 M€ from":
        selected_player = random.choice(which_option["players"])
        select_player_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "player",
                "player": selected_player
            }
        }
        print(waiting_for)
        print("selected player " + selected_player + " to remove 4 mc from")
        res = send_player_input(json.dumps(select_player_data), player.id)
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
    elif which_option["title"]["message"] == "Fund an award (${0} M€)":
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
    elif which_option["title"]["message"] == "Steal ${0} steel from ${1}":
        steal_steel_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(steal_steel_data), player.id)
        print("stole steel: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add ${0} microbes to ${1}":
        add_microbes_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_microbes_data), player.id)
        print("added microbes: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add resource to card ${0}":
        add_resource_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_resource_data), player.id)
        print("added resource to card: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add ${0} animals to ${1}":
        add_animals_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_animals_data), player.id)
        print("added animals: " + which_option["title"]["message"])
        return res
    else:
        print("LOOK HERE 1234 not implemented")
        print(which_option)
        exit(-1)

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
    #print(game)
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

    while "waitingFor" in res and res["game"]["phase"] == "research":
        if "title" in res["waitingFor"] and "message" in res["waitingFor"]["title"]:
            if res["waitingFor"]["title"]["message"].startswith("Select how to spend"):
                if res["waitingFor"]["paymentOptions"]["heat"]:
                    cost = res["waitingFor"]["amount"]
                    available_heat = game["thisPlayer"]["heat"]
                    #available_mc = game["thisPlayer"]["megaCredits"]
                    pay_heat = cost
                    pay_mc = 0
                    if cost > available_heat:
                        pay_heat = available_heat
                        pay_mc = cost - pay_heat
                        #print("not enough heat. other options: " + str(res["waitingFor"]["paymentOptions"]))


                    select_payment_data = {
                        "runId": player.run_id,
                        "type": "payment",
                        "payment": {
                            "heat": pay_heat,
                            "megaCredits": pay_mc,
                            "steel": 0,
                            "titanium": 0,
                            "plants": 0,
                            "microbes": 0,
                            "floaters": 0,
                            "lunaArchivesScience": 0,
                            "spireScience": 0,
                            "seeds": 0,
                            "auroraiData": 0,
                            "graphene": 0,
                            "kuiperAsteroids": 0,
                            "corruption": 0
                        }
                    }
                    res = send_player_input(json.dumps(select_payment_data), player.id)
                    print("payed with heat")
                    print(res)
                #print("select how to spend in research phase is not yet implemented")
                #print(card_selection)
                #print(res["waitingFor"])
                #exit(-1)
                else:
                    print("not heat")
                    print(res["waitingFor"])
                    exit(-1)
            else:
                print("different problem v9n(Q§ZV)$(Z")
                print(res["waitingFor"])
                exit(-1)
        else:
            print("different problem sk0ö03a4h6")
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
