import math
import random
import json

SPACE_CARDS = ",Space Hotels,Point Luna,Orbital Construction Yard,Space Elevator,Aerobraked Ammonia Asteroid,Asteroid,Asteroid Mining,Beam From A Thorium Asteroid,Big Asteroid,Callisto Penal Mines,Comet,Convoy From Europa,Deimos Down,Ganymede Colony,Giant Ice Asteroid,Giant Space Mirror,Ice Asteroid,Immigration Shuttles,Imported GHG,Imported Hydrogen,Imported Nitrogen,Import of Advanced GHG,Interstellar Colony Ship,Io Mining Industries,Lagrange Observatory,Large Convoy,Methane From Titan,Miranda Resort,Nitrogen-Rich Asteroid,Optimal Aerobraking,Phobos Space Haven,Satellites,Security Fleet,Shuttles,Solar Wind Power,Soletta,Space Mirrors,Space Station,Technology Demonstration,Terraforming Ganymede,Toll Station,Towing A Comet,Trans-Neptune Probe,Vesta Shipyard,Water Import From Europa,"

BUILDING_CARDS = ",Smelting Plant,SF Memorial,Self-Sufficient Settlement,Polar Industries,Mohole Excavation,Mohole,Mining Operations,Martian Industries,Lava Tube Settlement,House Printing,Early Settlement,Dome Farming,Cheung Shing MARS,AI Central,Aquifer Pumping,Artificial Lake,Biomass Combustors,Building Industries,Capital,Carbonate Processing,Colonizer Training Camp,Commercial District,Corporate Stronghold,Cupola City,Deep Well Heating,Development Center,Domed Crater,Electro Catapult,Eos Chasma National Park,Equatorial Magnetizer,Food Factory,Fueled Generators,Fuel Factory,Fusion Power,Geothermal Power,GHG Factories,Great Dam,Greenhouses,Heat Trappers,Immigrant City,Industrial Center,Industrial Microbes,Ironworks,Magnetic Field Dome,Magnetic Field Generators,Mars University,Martian Rails,Medical Lab,Mine,Mining Area,Mining Rights,Mining Rights,Mining Rights,Mohole Area,Natural Preserve,Noctis City,Noctis Farming,Nuclear Power,Olympus Conference,Open City,Ore Processor,Peroxide Power,Physics Complex,Power Infrastructure,Power Plant,,Protected Valley,Rad-Chem Factory,Research Outpost,Rover Construction,Soil Factory,Solar Power,Space Elevator,Steelworks,Strip Mine,Tectonic Stress Power,Titanium Mine,Tropical Resort,Underground City,Underground Detonations,Urbanized Area,Water Splitting Plant,Windmills,"

PLANT_CARDS = ",Biosphere Support,Dome Farming,Ecology Experts,Experimental Forest,Adapted Lichen,Advanced Ecosystems,Algae,Arctic Algae,Bushes,Ecological Zone,Eos Chasma National Park,Farming,Grass,Greenhouses,Heather,Kelp Farming,Lichen,Mangrove,Moss,Nitrophilic Moss,Noctis Farming,Plantation,Protected Valley,Trees,Tundra Farming,"

#http_connection = http.client.HTTPConnection("localhost", 8080)

# analog zu in "/new-game" auf "create game" zu klicken
def create_game(http_connection):
    settings = {
        "players": [
            {
                "name": "YellowPlayer",
                "color": "yellow",
                "beginner": False,
                "handicap": 0,
                "first": False
            },
            {
                "name": "RedPlayer",
                "color": "red",
                "beginner": False,
                "handicap": 0,
                "first": False
            },
            {
                "name": "GreenPlayer",
                "color": "green",
                "beginner": False,
                "handicap": 0,
                "first": False
            }
        ],
        "corporateEra": True,
        "prelude": True,
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
        "seed": random.random(),
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


def send_player_input(json_body, player_id, http_connection):
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("POST", "/player/input?id=" + player_id, body=json_body)
    response = http_connection.getresponse()
    return json.loads(response.read().decode())


# research phase
def initial_research_phase(player, http_connection):
    game = get_game(player.id, http_connection)
    player.run_id = game["runId"]
    # print("run id: " + player.run_id + " player id: " + player.id)
    #print(json.dumps(game, indent=4))
    #exit(48574985)

    res = turn(player, http_connection)
    return res

    corporation_selection = random.randint(0, 1)
    available_corporations = game["dealtCorporationCards"]
    corporation_name = available_corporations[corporation_selection]["name"]

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
        "Saturn Systems": 42,
        "Teractor": 60,
        "Cheung Shing MARS": 44,
        "Point Luna": 38,
        "Robinson Industries": 47,
        "Valley Trust": 37,
        "Vitor": 45,
    }
    available_cash = startingMegaCredits[corporation_name]
    #card_selection = list()
    while True:
        cardssss = game["waitingFor"]["options"][2]["cards"]
        card_selection = random.sample(cardssss, random.randint(0, 10))
        card_cost = sum(map(lambda card: card["calculatedCost"], card_selection))
        if card_cost <= available_cash:
            break
        #print("too expensive, draw again")

    project_card_names_selection = list(
        map(
            lambda card: card["name"], card_selection))

    available_prelude_cards = game["waitingFor"]["options"][1]["cards"]
    selected_prelude_cards = random.sample(available_prelude_cards, 2)
    prelude_cards_names_selection = list(map(lambda card: card["name"], selected_prelude_cards))

    buy_initial_cards = {
        "runId": player.run_id,
        "type": "initialCards",
        "responses": [
            {
                "type": "card",
                "cards": [corporation_name]
            }, {
                "type": "card",
                "cards": prelude_cards_names_selection
            }, {
                "type": "card",
                "cards": project_card_names_selection
            }]
    }

    #print("player " + player.name + " chose corporation (" + str(available_cash) + " MC)" + game["dealtCorporationCards"][corporation]["name"] + " and drew these cards: " + str(card_names_selection))

    buy_initial_cards_json = json.dumps(buy_initial_cards)
    res = send_player_input(buy_initial_cards_json, player.id, http_connection)
    #print(res)
    #print("phase: " + res["game"]["phase"])
    player.game_age = res["game"]["gameAge"]
    player.undo_count = res["game"]["undoCount"]
    #is_waiting = waiting_for(player)
    #print(is_waiting)
    return res

def waiting_for(player, http_connection):
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("GET", "/api/waitingfor?id=" + player.id + "&gameAge=" + str(player.game_age) + "&undoCount=" + str(player.undo_count))
    response = http_connection.getresponse()
    return json.loads(response.read().decode())

def get_game(player_id, http_connection):
    #connection = http.client.HTTPConnection("localhost", 8080)
    http_connection.request("GET", "/api/player?id=" + player_id)
    response = http_connection.getresponse()
    return json.loads(response.read().decode())

def turn(player, http_connection):
    #print("turn of " + player.name)
    game = get_game(player.id, http_connection)
    #print("generation: " + str(game["game"]["generation"]))
    if "waitingFor" not in game:
        print("waiting for not in game warum auch immer")
        print(game)
        exit(-1)
    waiting_for = game["waitingFor"]

    if "options" not in waiting_for:
        #print(waiting_for["title"])
        if "message" in waiting_for["title"]:
            if waiting_for["title"]["message"] == "Select space for ${0} tile":
                tile_to_place_name = waiting_for["title"]["data"][0]["value"]
                available_spaces = waiting_for["spaces"]
                selected_space = random.choice(available_spaces)
                select_space_data = {
                    "runId": player.run_id,
                    "type": "space",
                    "spaceId": selected_space
                }
                res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
                #print("Select space")
                return res
            elif waiting_for["title"]["message"] == "Select player to decrease ${0} production by ${1} step(s)":
                which_production = waiting_for["title"]["data"][0]["value"]
                steps = waiting_for["title"]["data"][1]["value"]
                selected_player = random.choice(waiting_for["players"])
                pass_data = {
                    "runId": player.run_id,
                    "type": "player",
                    "player": selected_player
                }
                #print(waiting_for)
                #print("selected player " + selected_player + " to decrease")
                res = send_player_input(json.dumps(pass_data), player.id, http_connection)
                return res
            elif waiting_for["title"]["message"] == "Select card to add ${0} ${1}":
                add_amount = waiting_for["title"]["data"][0]["value"] # scheinbar immer 1
                add_what = waiting_for["title"]["data"][1]["value"] # resources, Microbe,
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
                res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
                #print("selected card to add resources" + str(card_names_selection))
                return res
            elif waiting_for["title"]["message"] == "Select how to pay for the ${0} standard project":
                which_standard_project = waiting_for["title"]["data"][0]["value"] # type 3
                #print(waiting_for["title"])
                #exit(-1)
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
                # available_plants = game["thisPlayer"]["plants"]

                available_payments = ["mc"]  # can always pay with mc
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

                remaining_cost = cost
                for payment in available_payments:
                    if remaining_cost <= 0:
                        break
                    elif payment == "mc":
                        if available_mc >= remaining_cost:
                            pay_mc = remaining_cost
                            break
                        else:
                            pay_mc = available_mc
                            remaining_cost = remaining_cost - available_mc
                    elif payment == "heat":
                        if available_heat >= remaining_cost:
                            pay_heat = remaining_cost
                            break
                        else:
                            pay_heat = available_heat
                            remaining_cost = remaining_cost - available_heat
                    elif payment == "steel":
                        if available_steel * steel_value >= remaining_cost:
                            pay_steel = math.ceil(remaining_cost / steel_value)
                            break
                        else:
                            pay_steel = available_steel
                            remaining_cost = remaining_cost - available_steel * steel_value
                    elif payment == "titanium":
                        if available_titanium * titanium_value >= remaining_cost:
                            pay_titanium = math.ceil(remaining_cost / titanium_value)
                            break
                        else:
                            pay_titanium = available_titanium
                            remaining_cost = remaining_cost - available_titanium * titanium_value

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
                res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                #print("payed for standard project with heat/megacredits")
                return res
            elif waiting_for["title"]["message"] == "Select how to spend ${0} M€":
                amount_megacredits = waiting_for["title"]["data"][0]["value"]  # type 1 # immer 3??
                # exit(-1)
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
                # available_plants = game["thisPlayer"]["plants"]

                available_payments = ["mc"]  # can always pay with mc
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

                remaining_cost = cost
                for payment in available_payments:
                    if remaining_cost <= 0:
                        break
                    elif payment == "mc":
                        if available_mc >= remaining_cost:
                            pay_mc = remaining_cost
                            break
                        else:
                            pay_mc = available_mc
                            remaining_cost = remaining_cost - available_mc
                    elif payment == "heat":
                        if available_heat >= remaining_cost:
                            pay_heat = remaining_cost
                            break
                        else:
                            pay_heat = available_heat
                            remaining_cost = remaining_cost - available_heat
                    elif payment == "steel":
                        if available_steel * steel_value >= remaining_cost:
                            pay_steel = math.ceil(remaining_cost / steel_value)
                            break
                        else:
                            pay_steel = available_steel
                            remaining_cost = remaining_cost - available_steel * steel_value
                    elif payment == "titanium":
                        if available_titanium * titanium_value >= remaining_cost:
                            pay_titanium = math.ceil(remaining_cost / titanium_value)
                            break
                        else:
                            pay_titanium = available_titanium
                            remaining_cost = remaining_cost - available_titanium * titanium_value

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
                res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                # print("payed for standard project with heat/megacredits")
                return res
            elif waiting_for["title"]["message"].startswith("Select how to pay for") and waiting_for["title"]["message"].endswith("milestone"):
                print("if this happens this cant be removed") # TODO looks like this can be removed
                print(waiting_for["title"])
                exit(-1)
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
                # available_plants = game["thisPlayer"]["plants"]

                available_payments = ["mc"]  # can always pay with mc
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

                remaining_cost = cost
                for payment in available_payments:
                    if remaining_cost <= 0:
                        break
                    elif payment == "mc":
                        if available_mc >= remaining_cost:
                            pay_mc = remaining_cost
                            break
                        else:
                            pay_mc = available_mc
                            remaining_cost = remaining_cost - available_mc
                    elif payment == "heat":
                        if available_heat >= remaining_cost:
                            pay_heat = remaining_cost
                            break
                        else:
                            pay_heat = available_heat
                            remaining_cost = remaining_cost - available_heat
                    elif payment == "steel":
                        if available_steel * steel_value >= remaining_cost:
                            pay_steel = math.ceil(remaining_cost / steel_value)
                            break
                        else:
                            pay_steel = available_steel
                            remaining_cost = remaining_cost - available_steel * steel_value
                    elif payment == "titanium":
                        if available_titanium * titanium_value >= remaining_cost:
                            pay_titanium = math.ceil(remaining_cost / titanium_value)
                            break
                        else:
                            pay_titanium = available_titanium
                            remaining_cost = remaining_cost - available_titanium * titanium_value

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

                res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                #print("payed for milestone with heat/megacredits")
                return res
            elif waiting_for["title"]["message"] == "Select how to spend ${0} M€ for ${1} cards":

                how_much_mc = waiting_for["title"]["data"][0]["value"] # type 1
                how_many_cards = waiting_for["title"]["data"][1]["value"] # type 1
                # print(how_much_mc, how_many_cards) # scheinbar immer 3 1,

                # looks like this only happens for helion
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
                res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                #print("spent for card heat/megacredits")
                return res
            elif waiting_for["title"]["message"] == "Select how to pay for ${0} action":
                which_card_name = waiting_for["title"]["data"][0]["value"] # type 3

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
                # available_plants = game["thisPlayer"]["plants"]

                available_payments = ["mc"]  # can always pay with mc
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

                remaining_cost = cost
                for payment in available_payments:
                    if remaining_cost <= 0:
                        break
                    elif payment == "mc":
                        if available_mc >= remaining_cost:
                            pay_mc = remaining_cost
                            break
                        else:
                            pay_mc = available_mc
                            remaining_cost = remaining_cost - available_mc
                    elif payment == "heat":
                        if available_heat >= remaining_cost:
                            pay_heat = remaining_cost
                            break
                        else:
                            pay_heat = available_heat
                            remaining_cost = remaining_cost - available_heat
                    elif payment == "steel":
                        if available_steel * steel_value >= remaining_cost:
                            pay_steel = math.ceil(remaining_cost / steel_value)
                            break
                        else:
                            pay_steel = available_steel
                            remaining_cost = remaining_cost - available_steel * steel_value
                    elif payment == "titanium":
                        if available_titanium * titanium_value >= remaining_cost:
                            pay_titanium = math.ceil(remaining_cost / titanium_value)
                            break
                        else:
                            pay_titanium = available_titanium
                            remaining_cost = remaining_cost - available_titanium * titanium_value

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

                #print(str(cost) + "b56zn payed: " + str(json.dumps(select_payment_data)))
                res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                #print("payed for action with heat/megacredits/steel/titanium")
                return res
            elif waiting_for["title"]["message"] == "Select a card to keep and pass the rest to ${0}":
                card_selection = random.choice(waiting_for["cards"])["name"]
                draw_data = {
                    "runId": player.run_id,
                    "type": "card",
                    "cards": [card_selection]
                }
                res = send_player_input(json.dumps(draw_data), player.id, http_connection)
                return res
            else:
                print("LOOK HERE options message not yet implemented")
                print(waiting_for)
                exit(-1)
        elif waiting_for["title"] == "Select space for ocean tile":

            #hier zuletzt
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Select space")
            return res
        elif waiting_for["title"] == "Select space reserved for ocean to place greenery tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Select space reserved for ocean to place greenery tile")
            return res
        elif waiting_for["title"] == "Select how to pay for award":
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
            # available_plants = game["thisPlayer"]["plants"]

            available_payments = ["mc"]  # can always pay with mc
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

            remaining_cost = cost
            for payment in available_payments:
                if remaining_cost <= 0:
                    break
                elif payment == "mc":
                    if available_mc >= remaining_cost:
                        pay_mc = remaining_cost
                        break
                    else:
                        pay_mc = available_mc
                        remaining_cost = remaining_cost - available_mc
                elif payment == "heat":
                    if available_heat >= remaining_cost:
                        pay_heat = remaining_cost
                        break
                    else:
                        pay_heat = available_heat
                        remaining_cost = remaining_cost - available_heat
                elif payment == "steel":
                    if available_steel * steel_value >= remaining_cost:
                        pay_steel = math.ceil(remaining_cost / steel_value)
                        break
                    else:
                        pay_steel = available_steel
                        remaining_cost = remaining_cost - available_steel * steel_value
                elif payment == "titanium":
                    if available_titanium * titanium_value >= remaining_cost:
                        pay_titanium = math.ceil(remaining_cost / titanium_value)
                        break
                    else:
                        pay_titanium = available_titanium
                        remaining_cost = remaining_cost - available_titanium * titanium_value

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

            res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
            #print("payed for award project with heat/megacredits/steel/titanium")
            return res
        elif waiting_for["title"] == "Select a space with a steel or titanium bonus":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected space with a steel or titanium bonus (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space adjacent to a city tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected space adjacent to a city tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select builder card to copy":
            available_cards = waiting_for["cards"]
            selected_card = random.choice(available_cards)
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": [selected_card["name"]]
            }
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("Selected builder card to copy (" + selected_card["name"] + ")")
            return res
        elif waiting_for["title"] == "Select place next to no other tile for city":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected place next to no other tile for city (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select 1 card(s) to keep":
            available_cards = waiting_for["cards"]
            selected_card = random.choice(available_cards)
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": [selected_card["name"]]
            }
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("Selected card to keep (" + selected_card["name"] + ")")
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("Selected cards to keep (" + str(card_names_selection) + ")")
            return res
        elif waiting_for["title"] == "Select space next to greenery for special tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected space next to greenery for special tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select a space with a steel or titanium bonus adjacent to one of your tiles":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected a space with a steel or titanium bonus adjacent to one of your tiles (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space next to at least 2 other city tiles":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Select space next to at least 2 other city tiles (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select a land space to place an ocean tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            #print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for city tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for greenery tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for ocean from temperature increase":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for claim":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for first ocean":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for second ocean":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
            return res
        elif waiting_for["title"] == "Select space for special city tile":
            available_spaces = waiting_for["spaces"]
            select_space_data = {
                "runId": player.run_id,
                "type": "space",
                "spaceId": random.choice(available_spaces)
            }
            res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
            # print("Selected a land space to place an ocean tile (" + str(select_space_data["spaceId"]) + ")")
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
            res = send_player_input(json.dumps(select_decrease_amount_data), player.id, http_connection)
            #print("decreased heat production by " + str(decrease_amount))
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
            res = send_player_input(json.dumps(select_spend_amount_data), player.id, http_connection)
            #print("spent amount of energy " + str(spend_amount))
            return res
        elif waiting_for["title"] == "Select card(s) to buy":
            available_cards = waiting_for["cards"]
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 0 or max != 1:
                #print(waiting_for)
                #print("problem 87wzv89w489v4ö09")
                #exit(-1)
                pass

            sample = random.sample(available_cards, random.randint(min, max))
            card_names_selection = list(
                map(
                    lambda card: card["name"], sample))
            select_card_data = {
                "runId": player.run_id,
                "type": "card",
                "cards": card_names_selection
            }
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("selected card to buy" + str(card_names_selection))
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("selected card to remove microbe" + str(card_names_selection))
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
            #available_plants = game["thisPlayer"]["plants"]

            available_payments = ["mc"] # can always pay with mc
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

            remaining_cost = cost
            for payment in available_payments:
                if remaining_cost <= 0:
                    break
                elif payment == "mc":
                    if available_mc >= remaining_cost:
                        pay_mc = remaining_cost
                        break
                    else:
                        pay_mc = available_mc
                        remaining_cost = remaining_cost - available_mc
                elif payment == "heat":
                    if available_heat >= remaining_cost:
                        pay_heat = remaining_cost
                        break
                    else:
                        pay_heat = available_heat
                        remaining_cost = remaining_cost - available_heat
                elif payment == "steel":
                    if available_steel * steel_value >= remaining_cost:
                        pay_steel = math.ceil(remaining_cost/steel_value)
                        break
                    else:
                        pay_steel = available_steel
                        remaining_cost = remaining_cost - available_steel * steel_value
                elif payment == "titanium":
                    if available_titanium * titanium_value >= remaining_cost:
                        pay_titanium = math.ceil(remaining_cost/titanium_value)
                        break
                    else:
                        pay_titanium = available_titanium
                        remaining_cost = remaining_cost - available_titanium * titanium_value

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

            #print(str(cost) + " o8om8m payed: " + str(json.dumps(select_payment_data)))
            res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
            #print("payed for action with heat or titanium or steel")
            return res
        elif waiting_for["title"] == "Select how to pay for milestone":
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
            # available_plants = game["thisPlayer"]["plants"]

            available_payments = ["mc"]  # can always pay with mc
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

            remaining_cost = cost
            for payment in available_payments:
                if remaining_cost <= 0:
                    break
                elif payment == "mc":
                    if available_mc >= remaining_cost:
                        pay_mc = remaining_cost
                        break
                    else:
                        pay_mc = available_mc
                        remaining_cost = remaining_cost - available_mc
                elif payment == "heat":
                    if available_heat >= remaining_cost:
                        pay_heat = remaining_cost
                        break
                    else:
                        pay_heat = available_heat
                        remaining_cost = remaining_cost - available_heat
                elif payment == "steel":
                    if available_steel * steel_value >= remaining_cost:
                        pay_steel = math.ceil(remaining_cost / steel_value)
                        break
                    else:
                        pay_steel = available_steel
                        remaining_cost = remaining_cost - available_steel * steel_value
                elif payment == "titanium":
                    if available_titanium * titanium_value >= remaining_cost:
                        pay_titanium = math.ceil(remaining_cost / titanium_value)
                        break
                    else:
                        pay_titanium = available_titanium
                        remaining_cost = remaining_cost - available_titanium * titanium_value

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

            res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
            #print("payed for milestone with heat/megacredits")
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("couldnt afford any cards")
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            #print("selected card to remove 1 animal from" + str(card_names_selection))
            return res
        elif waiting_for["title"] == "Select prelude card to play":
            available_cards = waiting_for["cards"]
            max = waiting_for["max"]
            min = waiting_for["min"]
            if min != 1 or max != 1:
                print(waiting_for)
                print("problem qc2qce8q34hbv598ezqzqceq2")
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            # print("selected card to remove 1 animal from" + str(card_names_selection))
            return res
        elif waiting_for["title"] == "Play project card":
            playable_cards = waiting_for["cards"]
            random_card = random.choice(playable_cards)
            card_cost = random_card["calculatedCost"]
            reserve_units = random_card["reserveUnits"] if "reserveUnits" in random_card else None

            can_pay_with_steel = False  # building cards
            if BUILDING_CARDS.find(
                    "," + random_card["name"] + ",") != -1:  # the commas prevent 'Research' to match 'Research Outpost'
                can_pay_with_steel = True

            can_pay_with_titanium = False  # space cards
            if SPACE_CARDS.find(
                    "," + random_card["name"] + ",") != -1:  # the commas prevent 'Research' to match 'Research Outpost'
                can_pay_with_titanium = True

            payment_options = waiting_for["paymentOptions"]
            can_pay_with_heat = payment_options["heat"]

            can_pay_with_microbes = False
            for p in game["players"]:
                if p["name"] == player.name:
                    for card in p["tableau"]:
                        if card["name"] == "Psychrophiles":
                            if PLANT_CARDS.find("," + random_card["name"] + ",") != -1:
                                can_pay_with_microbes = True
                                break

            available_payments = ["mc"]  # can always pay with mc
            if can_pay_with_heat:
                available_payments.append("heat")
            if can_pay_with_steel:
                available_payments.append("steel")
            if can_pay_with_titanium:
                available_payments.append("titanium")
            if can_pay_with_microbes:
                available_payments.append("microbes")

            # generate order
            random.shuffle(available_payments)

            available_heat = game["thisPlayer"]["heat"]
            available_mc = game["thisPlayer"]["megaCredits"]
            available_steel = game["thisPlayer"]["steel"]
            steel_value = game["thisPlayer"]["steelValue"]
            available_titanium = game["thisPlayer"]["titanium"]
            titanium_value = game["thisPlayer"]["titaniumValue"]
            available_microbes = waiting_for["microbes"]
            microbe_value = 2

            if reserve_units is not None:
                available_heat -= reserve_units["heat"]
                available_mc -= reserve_units["megacredits"]
                available_titanium -= reserve_units["titanium"]
                available_steel -= reserve_units["steel"]

            pay_mc = 0
            pay_heat = 0
            pay_steel = 0
            pay_titanium = 0
            pay_microbes = 0

            remaining_cost = card_cost
            for payment in available_payments:
                if remaining_cost <= 0:
                    break
                elif payment == "mc":
                    if available_mc >= remaining_cost:
                        pay_mc = remaining_cost
                        break
                    else:
                        pay_mc = available_mc
                        remaining_cost = remaining_cost - available_mc
                elif payment == "heat":
                    if available_heat >= remaining_cost:
                        pay_heat = remaining_cost
                        break
                    else:
                        pay_heat = available_heat
                        remaining_cost = remaining_cost - available_heat
                elif payment == "steel":
                    if available_steel * steel_value >= remaining_cost:
                        pay_steel = math.ceil(remaining_cost / steel_value)
                        break
                    else:
                        pay_steel = available_steel
                        remaining_cost = remaining_cost - available_steel * steel_value
                elif payment == "titanium":
                    if available_titanium * titanium_value >= remaining_cost:
                        pay_titanium = math.ceil(remaining_cost / titanium_value)
                        break
                    else:
                        pay_titanium = available_titanium
                        remaining_cost = remaining_cost - available_titanium * titanium_value
                elif payment == "microbes":
                    if available_microbes * microbe_value >= remaining_cost:
                        pay_microbes = math.ceil(remaining_cost / microbe_value)
                        break
                    else:
                        pay_microbes = available_microbes
                        remaining_cost = remaining_cost - available_microbes * microbe_value

            select_card_data = {
                "runId": player.run_id,
                "type": "projectCard",
                "card": random_card["name"],
                "payment": {
                    "heat": pay_heat,
                    "megaCredits": pay_mc,
                    "steel": pay_steel,
                    "titanium": pay_titanium,
                    "plants": 0,
                    "microbes": pay_microbes,
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
            res = send_player_input(json.dumps(select_card_data), player.id, http_connection)
            # print("selected card to remove 1 animal from" + str(card_names_selection))
            return res
        else:
            print("LOOK HERE options title not yet implemented")
            print(waiting_for)
            exit(-1)
    #else:
        #options is in waiting for

    if waiting_for["title"] == "Initial Research Phase":
        corporation_selection = random.randint(0, 1)
        available_corporations = game["dealtCorporationCards"]
        corporation_name = available_corporations[corporation_selection]["name"]

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
            "Saturn Systems": 42,
            "Teractor": 60,
            "Cheung Shing MARS": 44,
            "Point Luna": 38,
            "Robinson Industries": 47,
            "Valley Trust": 37,
            "Vitor": 45,
        }
        available_cash = startingMegaCredits[corporation_name]

        while True:
            cardssss = game["waitingFor"]["options"][2]["cards"]
            card_selection = random.sample(cardssss, random.randint(0, 10))
            card_cost = sum(map(lambda card: card["calculatedCost"], card_selection))
            if card_cost <= available_cash:
                break
            # print("too expensive, draw again")

        project_card_names_selection = list(
            map(
                lambda card: card["name"], card_selection))

        available_prelude_cards = game["waitingFor"]["options"][1]["cards"]
        selected_prelude_cards = random.sample(available_prelude_cards, 2)
        prelude_cards_names_selection = list(map(lambda card: card["name"], selected_prelude_cards))

        buy_initial_cards = {
            "runId": player.run_id,
            "type": "initialCards",
            "responses": [
                {
                    "type": "card",
                    "cards": [corporation_name]
                }, {
                    "type": "card",
                    "cards": prelude_cards_names_selection
                }, {
                    "type": "card",
                    "cards": project_card_names_selection
                }]
        }

        buy_initial_cards_json = json.dumps(buy_initial_cards)
        res = send_player_input(buy_initial_cards_json, player.id, http_connection)
        return res

    standard_projects_count = 5
    which_standard_project = random.randint(0, standard_projects_count-1)

    which_option = waiting_for["options"][0] # initialization
    while True:
        action_index = random.randint(0, len(waiting_for["options"]) - 1) # choose random index
        which_option = waiting_for["options"][action_index]
        if which_option["title"] == "Standard projects":
            available_heat = game["thisPlayer"]["heat"]
            available_mc = game["thisPlayer"]["megaCredits"]
            selected_standard_project_cost = which_option["cards"][which_standard_project]["calculatedCost"]
            #print("selected " + which_option["cards"][which_standard_project]["name"])
            #print("cost: " + str(which_option["cards"][which_standard_project]["calculatedCost"]))
            is_helion = game["pickedCorporationCard"][0]["name"] == "Helion"
            if is_helion:
                if available_heat + available_mc >= selected_standard_project_cost:
                    #print("is helion " + str(available_mc) + str(available_mc))
                    break
            else:
                if available_mc >= selected_standard_project_cost:
                    #print("is not helion " + str(available_mc))
                    break
        else:
            break

    if which_option["title"] == "Pass for this generation":
        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        #print("passed")
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Play project card":
        playable_cards = which_option["cards"]
        random_card = random.choice(playable_cards)
        card_cost = random_card["calculatedCost"]
        reserve_units = random_card["reserveUnits"] if "reserveUnits" in random_card else None

        can_pay_with_steel = False # building cards
        if BUILDING_CARDS.find(
                "," + random_card["name"] + ",") != -1: # the commas prevent 'Research' to match 'Research Outpost'
            can_pay_with_steel = True

        can_pay_with_titanium = False # space cards
        if SPACE_CARDS.find(
                "," + random_card["name"] + ",") != -1: # the commas prevent 'Research' to match 'Research Outpost'
            can_pay_with_titanium = True

        payment_options = which_option["paymentOptions"]

        can_pay_with_heat = payment_options["heat"]

        can_pay_with_microbes = False
        for p in game["players"]:
            if p["name"] == player.name:
                for card in p["tableau"]:
                    if card["name"] == "Psychrophiles":
                        if PLANT_CARDS.find("," + random_card["name"] + ",") != -1:
                            can_pay_with_microbes = True
                            break

        available_payments = ["mc"]  # can always pay with mc
        if can_pay_with_heat:
            available_payments.append("heat")
        if can_pay_with_steel:
            available_payments.append("steel")
        if can_pay_with_titanium:
            available_payments.append("titanium")
        if can_pay_with_microbes:
            available_payments.append("microbes")

        # generate order
        random.shuffle(available_payments)

        available_heat = game["thisPlayer"]["heat"]
        available_mc = game["thisPlayer"]["megaCredits"]
        available_steel = game["thisPlayer"]["steel"]
        steel_value = game["thisPlayer"]["steelValue"]
        available_titanium = game["thisPlayer"]["titanium"]
        titanium_value = game["thisPlayer"]["titaniumValue"]
        available_microbes = which_option["microbes"]
        microbe_value = 2

        if reserve_units is not None:
            available_heat -= reserve_units["heat"]
            available_mc -= reserve_units["megacredits"]
            available_titanium -= reserve_units["titanium"]
            available_steel -= reserve_units["steel"]

        pay_mc = 0
        pay_heat = 0
        pay_steel = 0
        pay_titanium = 0
        pay_microbes = 0

        remaining_cost = card_cost
        for payment in available_payments:
            if remaining_cost <= 0:
                break
            elif payment == "mc":
                if available_mc >= remaining_cost:
                    pay_mc = remaining_cost
                    break
                else:
                    pay_mc = available_mc
                    remaining_cost = remaining_cost - available_mc
            elif payment == "heat":
                if available_heat >= remaining_cost:
                    pay_heat = remaining_cost
                    break
                else:
                    pay_heat = available_heat
                    remaining_cost = remaining_cost - available_heat
            elif payment == "steel":
                if available_steel * steel_value >= remaining_cost:
                    pay_steel = math.ceil(remaining_cost / steel_value)
                    break
                else:
                    pay_steel = available_steel
                    remaining_cost = remaining_cost - available_steel * steel_value
            elif payment == "titanium":
                if available_titanium * titanium_value >= remaining_cost:
                    pay_titanium = math.ceil(remaining_cost / titanium_value)
                    break
                else:
                    pay_titanium = available_titanium
                    remaining_cost = remaining_cost - available_titanium * titanium_value
            elif payment == "microbes":
                if available_microbes * microbe_value >= remaining_cost:
                    pay_microbes = math.ceil(remaining_cost / microbe_value)
                    break
                else:
                    pay_microbes = available_microbes
                    remaining_cost = remaining_cost - available_microbes * microbe_value

        pass_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "projectCard",
                "card": random_card["name"],
                "payment": {
                    "heat":pay_heat,
                    "megaCredits": pay_mc,
                    "steel":pay_steel,
                    "titanium":pay_titanium,
                    "plants":0,
                    "microbes":pay_microbes,
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        if "message" in res and res["message"].startswith("Unknown"):
            print(game)
            print(res)
            print(playable_cards)
            print(random_card)
            print("playing project card threw an error (" + res["message"] + ")")
            print(pass_data)
            print(payment_options)
            print("available mc: " + str(available_mc))
            exit(-1)
            # TODO most likely a wrong error message thrown because conditions are not met -> retry
            return turn(player)
        elif "message" in res and res["message"] == "You do not have that many resources to spend":
            # e.g. Local Heat Trapping
            print(game)
            print(res)
            print(res["message"])
            print(playable_cards)
            print("Card costs: " + str(random_card["calculatedCost"]))
            print(game["thisPlayer"])
            print(payment_options)
            print(pass_data)
            print("available mc: " + str(available_mc))
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
            print("available mc: " + str(available_mc))
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
            print("available mc: " + str(available_mc))
            exit(-1)
            return turn(player)
        elif "message" in res:
            print("other message juhf984zt9e8th9e84t: " + res["message"])
            print(game["thisPlayer"])
            print(payment_options)
            print("available mc: " + str(available_mc))
            exit(-1)
        #print("play project card")
        return res
    elif which_option["title"] == "Standard projects":
        # TODO only select standard project if resources are available
        selected_standard_project = which_option["cards"][which_standard_project]["name"]
        standard_project_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "card",
                "cards": [selected_standard_project]
            }
        }
        res = send_player_input(json.dumps(standard_project_data), player.id, http_connection)
        #print("standard project (" + selected_standard_project + ")")
        if "message" in res and res["message"].endswith("not available"):
            #print("retry because buying standard project threw error (" + res["message"] + ")")
            # essentially a hacky retry
            #print(game)
            #print(game["game"]["spaces"])
            #print(game["thisPlayer"])
            #print(waiting_for)
            #print(which_option)
            #print(which_option["cards"])
            #print(game["id"])
            #exit(-1)
            # maybe this is because no more space is available for a city
            print("No space left to place " + selected_standard_project + " 9sv8z9abüaöe9b " + res["message"])
            return turn(player, http_connection)
        return res
    elif which_option["title"] == "Sell patents":
        project_cards = which_option["cards"]
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("sell patents")
        #print(res)
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
        res = send_player_input(json.dumps(end_turn_data), player.id, http_connection)
        #print("End turn")
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
        res = send_player_input(json.dumps(convert_heat_data), player.id, http_connection)
        #print("Convert heat into temperature")
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
        res = send_player_input(json.dumps(convert_plants_data), player.id, http_connection)
        #print("Convert plants into greenery")
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
        res = send_player_input(json.dumps(perform_card_action_data), player.id, http_connection)
        #print("Performing card action")
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
        #print("Do nothing")
        res = send_player_input(json.dumps(do_nothing_data), player.id, http_connection)
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
        #print("Claim a milestone")
        res = send_player_input(json.dumps(claim_milestone_data), player.id, http_connection)
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
        #print("Skipped removal")
        res = send_player_input(json.dumps(skip_removal_data), player.id, http_connection)
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
        #print("Skipped removing plants")
        res = send_player_input(json.dumps(skip_removal_data), player.id, http_connection)
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
        #print("Increased plant production 1 step")
        res = send_player_input(json.dumps(increase_plant_production_data), player.id, http_connection)
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("Selected a card to discard (" + selected_card["name"] + ")")
        #print(res)
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
        #print("Added a science resource to this card")
        res = send_player_input(json.dumps(add_science_data), player.id, http_connection)
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
        #print("Didnt remove resource")
        res = send_player_input(json.dumps(dont_remove_data), player.id, http_connection)
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
        #print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_energy_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase titanium production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase megacredits production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase steel production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase plants production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase heat production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Increase energy production 1 step":
        increase_production_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("Increased energy production 2 steps")
        res = send_player_input(json.dumps(increase_production_data), player.id, http_connection)
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
        #print("Didn't steal")
        res = send_player_input(json.dumps(dont_steal_data), player.id, http_connection)
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
        #print("Removed 2 microbes to raise oxygen level 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id, http_connection)
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
        #print("Added 1 microbe to this card")
        res = send_player_input(json.dumps(add_microbe_data), player.id, http_connection)
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
        #print("Removed 3 microbes to increase your terraform rating 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id, http_connection)
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
        res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
        #print("Selected space to place greenery (" + selected_space + ")")
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
        #print("Didnt place a greenery")
        res = send_player_input(json.dumps(dont_place_greenery_data), player.id, http_connection)
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
        #print("Removed a science resource from this card to draw a card")
        res = send_player_input(json.dumps(remove_science_data), player.id, http_connection)
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
        #print("Spent 1 steel to gain 7 M€")
        res = send_player_input(json.dumps(spend_steel_data), player.id, http_connection)
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
        #print("Removed 2 microbes to raise temperature 1 step")
        res = send_player_input(json.dumps(remove_microbes_data), player.id, http_connection)
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("Added 3 microbes to a card (" + selected_card["name"] + ")")
        #print(res)
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("Added 2 microbes to a card (" + selected_card["name"] + ")")
        #print(res)
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("Removed 2 animals from card (" + selected_card["name"] + ")")
        #print(res)
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        #print("Selected card to add 2 animals (" + selected_card["name"] + ")")
        #print(res)
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
        #print("Gained 4 plants")
        res = send_player_input(json.dumps(gain_4_plants_data), player.id, http_connection)
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
        #print("Spent 1 plant to gain 7 M€")
        res = send_player_input(json.dumps(spent_plant_for_mc_data), player.id, http_connection)
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
        #print("Gained plant")
        res = send_player_input(json.dumps(gain_plant_data), player.id, http_connection)
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
        #print("Gained 1 plant")
        res = send_player_input(json.dumps(gain_1_plant_data), player.id, http_connection)
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
        #print("Gained 3 plant")
        res = send_player_input(json.dumps(gain_3_plants_data), player.id, http_connection)
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
        #print("Gained 5 plants")
        res = send_player_input(json.dumps(gain_5_plants_data), player.id, http_connection)
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
        #print("Didnt remove mc from adjacent player")
        res = send_player_input(json.dumps(dont_remove_mc_from_adjacent_player_data), player.id, http_connection)
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
        #print(waiting_for)
        #print("selected player " + selected_player + " to remove 4 mc from")
        res = send_player_input(json.dumps(select_player_data), player.id, http_connection)
        return res
    elif which_option["title"] == "Select card to add 4 animals":
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)
        # print("Selected card to add 2 animals (" + selected_card["name"] + ")")
        # print(res)
        return res
    elif which_option["title"] == "Add 2 animals to a card":
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
        res = send_player_input(json.dumps(pass_data), player.id, http_connection)

        return res
    elif "message" not in which_option["title"]:
        print("bdsg LOOK HERE: " + which_option["title"] + " is not yet implemented")
        print(game)
        print(which_option)
        exit(-1)
    elif which_option["title"]["message"] == "Take first action of ${0} corporation":
        corporation = which_option["title"]["data"][0]["value"]
        if corporation not in {"Valley Trust", "Inventrix", "Vitor", "Tharsis Republic"}:
            print(corporation)
        # the case for inventrix, ...
        take_action_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(take_action_data), player.id, http_connection)
        #print("Took first action")
        return res
    elif which_option["title"]["message"] == "Fund an award (${0} M€)":
        amount = which_option["title"]["data"][0]["value"]
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
        res = send_player_input(json.dumps(fund_award_data), player.id, http_connection)
        return res
    elif which_option["title"]["message"] == "Convert ${0} plants into greenery":
        amount = which_option["title"]["data"][0]["value"]
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
        res = send_player_input(json.dumps(select_space_data), player.id, http_connection)
        #print("Selected space to place greenery")
        return res
    elif which_option["title"]["message"] == "Remove ${0} plants from ${1}":
        amount_of_plants = which_option["title"]["data"][0]["value"]
        from_whom = which_option["title"]["data"][1]["value"]
        remove_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        #print("removed something: " + which_option["title"]["message"])
        res = send_player_input(json.dumps(remove_data), player.id, http_connection)
        return res
    elif which_option["title"]["message"] == "Remove ${0} ${1} from ${2}":
        amount_to_remove = which_option["title"]["data"][0]["value"]
        resource_to_remove = which_option["title"]["data"][1]["value"]
        from_whom = which_option["title"]["data"][2]["value"]
        remove_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        # print("removed something: " + which_option["title"]["message"])
        res = send_player_input(json.dumps(remove_data), player.id, http_connection)
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
        res = send_player_input(json.dumps(steal_data), player.id, http_connection)
        #print("stole megacredits: " + which_option["title"]["message"])
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
        res = send_player_input(json.dumps(steal_steel_data), player.id, http_connection)
        #print("stole steel: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add ${0} microbes to ${1}":
        amount = which_option["title"]["data"][0]["value"]
        which_card = which_option["title"]["data"][1]["value"]

        add_microbes_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_microbes_data), player.id, http_connection)
        #print("added microbes: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add resource to card ${0}":
        which_card = which_option["title"]["data"][0]["value"]
        add_resource_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_resource_data), player.id, http_connection)
        #print("added resource to card: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Add ${0} animals to ${1}":
        amount = which_option["title"]["data"][0]["value"]
        to_what = which_option["title"]["data"][1]["value"]
        add_animals_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_animals_data), player.id, http_connection)
        #print("added animals: " + which_option["title"]["message"])
        return res
    elif which_option["title"]["message"] == "Fund ${0} award":
        what_award = which_option["title"]["data"][0]["value"]
        add_animals_data = {
            "runId": player.run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "option"
            }
        }
        res = send_player_input(json.dumps(add_animals_data), player.id, http_connection)
        #print("added animals: " + which_option["title"]["message"])
        return res
    else:
        print("LOOK HERE 1234 not implemented")
        print(which_option)
        exit(-1)

def draft(player, http_connection):
    game = get_game(player.id, http_connection)
    #print("generation: " + str(game["game"]["generation"]))
    waiting_for = game["waitingFor"]
    card_selection = random.choice(waiting_for["cards"])["name"]
    draw_data = {
        "runId": player.run_id,
        "type": "card",
        "cards": [card_selection]
    }
    res = send_player_input(json.dumps(draw_data), player.id, http_connection)
    #print(res)
    #print("phase: " + res["game"]["phase"])
    return res


def research_phase(player, http_connection):
    game = get_game(player.id, http_connection)
    #print(game["waitingFor"])
    #exit(-1)
    #print(game)
    #print("generation: " + str(game["game"]["generation"]))
    card_selection = list(
        map(
            lambda card: card["name"], random.sample(game["waitingFor"]["cards"], random.randint(0, 4))))
    buy_cards_data = {
        "runId": player.run_id,
        "type": "card",
        "cards": card_selection
        #"cards": [game["waitingFor"]["cards"][0]["name"], game["waitingFor"]["cards"][1]["name"]]
    }
    res = send_player_input(json.dumps(buy_cards_data), player.id, http_connection)
    # TODO could be too expensive
    #print(res)

    while "waitingFor" in res and res["game"]["phase"] == "research":
        if "title" in res["waitingFor"] and "message" in res["waitingFor"]["title"]:
            if res["waitingFor"]["title"]["message"] == "Select how to spend ${0} M€ for ${1} cards":
                #print(res["waitingFor"])
                #exit(-1)
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
                    res = send_player_input(json.dumps(select_payment_data), player.id, http_connection)
                    #print("payed with heat")
                    #print(res)
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


def generation(first_player, second_player, third_player, http_connection):
    #print("new generation:")

    turn(first_player, http_connection)
    turn(second_player, http_connection)
    turn(third_player, http_connection)

    # order of the three is arbitrary
    draft(first_player, http_connection)
    draft(second_player, http_connection)
    draft(third_player, http_connection)

    # order of the three is arbitrary
    draft(first_player, http_connection)
    draft(second_player, http_connection)
    draft(third_player, http_connection)

    # order of the three is arbitrary
    draft(first_player, http_connection)
    draft(second_player, http_connection)
    draft(third_player, http_connection)

    # order of the three is arbitrary
    research_phase(first_player, http_connection)
    research_phase(second_player, http_connection)
    research_phase(third_player, http_connection)
