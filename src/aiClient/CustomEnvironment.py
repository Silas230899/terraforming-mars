import math
from enum import Enum
from typing import Dict

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import json
import random

from gymnasium.spaces import Box, Discrete, MultiBinary

from action_observation_names import *

BUILDING_CARDS_SET = {'Smelting Plant', 'SF Memorial', 'Self-Sufficient Settlement', 'Polar Industries', 'Mohole Excavation', 'Mohole', 'Mining Operations', 'Martian Industries', 'Lava Tube Settlement', 'House Printing', 'Early Settlement', 'Dome Farming', 'Cheung Shing MARS', 'AI Central', 'Aquifer Pumping', 'Artificial Lake', 'Biomass Combustors', 'Building Industries', 'Capital', 'Carbonate Processing', 'Colonizer Training Camp', 'Commercial District', 'Corporate Stronghold', 'Cupola City', 'Deep Well Heating', 'Development Center', 'Domed Crater', 'Electro Catapult', 'Eos Chasma National Park', 'Equatorial Magnetizer', 'Food Factory', 'Fueled Generators', 'Fuel Factory', 'Fusion Power', 'Geothermal Power', 'GHG Factories', 'Great Dam', 'Greenhouses', 'Heat Trappers', 'Immigrant City', 'Industrial Center', 'Industrial Microbes', 'Ironworks', 'Magnetic Field Dome', 'Magnetic Field Generators', 'Mars University', 'Martian Rails', 'Medical Lab', 'Mine', 'Mining Area', 'Mining Rights', 'Mining Rights', 'Mining Rights', 'Mohole Area', 'Natural Preserve', 'Noctis City', 'Noctis Farming', 'Nuclear Power', 'Olympus Conference', 'Open City', 'Ore Processor', 'Peroxide Power', 'Physics Complex', 'Power Infrastructure', 'Power Plant', 'Protected Valley', 'Rad-Chem Factory', 'Research Outpost', 'Rover Construction', 'Soil Factory', 'Solar Power', 'Space Elevator', 'Steelworks', 'Strip Mine', 'Tectonic Stress Power', 'Titanium Mine', 'Tropical Resort', 'Underground City', 'Underground Detonations', 'Urbanized Area', 'Water Splitting Plant', 'Windmills'}

SPACE_CARDS_SET = {'Space Hotels', 'Point Luna', 'Orbital Construction Yard', 'Space Elevator', 'Aerobraked Ammonia Asteroid', 'Asteroid', 'Asteroid Mining', 'Beam From A Thorium Asteroid', 'Big Asteroid', 'Callisto Penal Mines', 'Comet', 'Convoy From Europa', 'Deimos Down', 'Ganymede Colony', 'Giant Ice Asteroid', 'Giant Space Mirror', 'Ice Asteroid', 'Immigration Shuttles', 'Imported GHG', 'Imported Hydrogen', 'Imported Nitrogen', 'Import of Advanced GHG', 'Interstellar Colony Ship', 'Io Mining Industries', 'Lagrange Observatory', 'Large Convoy', 'Methane From Titan', 'Miranda Resort', 'Nitrogen-Rich Asteroid', 'Optimal Aerobraking', 'Phobos Space Haven', 'Satellites', 'Security Fleet', 'Shuttles', 'Solar Wind Power', 'Soletta', 'Space Mirrors', 'Space Station', 'Technology Demonstration', 'Terraforming Ganymede', 'Toll Station', 'Towing A Comet', 'Trans-Neptune Probe', 'Vesta Shipyard', 'Water Import From Europa'}

PLANT_CARDS_SET = {'Biosphere Support', 'Dome Farming', 'Ecology Experts', 'Experimental Forest', 'Adapted Lichen', 'Advanced Ecosystems', 'Algae', 'Arctic Algae', 'Bushes', 'Ecological Zone', 'Eos Chasma National Park', 'Farming', 'Grass', 'Greenhouses', 'Heather', 'Kelp Farming', 'Lichen', 'Mangrove', 'Moss', 'Nitrophilic Moss', 'Noctis Farming', 'Plantation', 'Protected Valley', 'Trees', 'Tundra Farming'}

NUMBER_CORPORATIONS = 12
NUMBER_PLAYERS = 3
NUMBER_OF_CARDS = 199
NUMBER_ALL_ACTION_OPTIONS = 58
NUMBER_ALL_ACTIONS = 38 # without action options
NUMBER_SPACES = 68 # indices 01 to 69

def NUMBER_OF_AWARDS(): return len(AWARDS_INT_STR.values())
def NUMBER_OF_MILESTONES(): return len(MILESTONES_INT_STR.values())
def NUMBER_OF_STANDARD_PROJECTS(): return len(STANDARD_PROJECTS_INDEX_NAME.values())

class PhasesEnum(Enum):
    INITIAL_RESEARCH = 0,
    RESEARCH = 1,
    ACTION = 2,
    PRODUCTION = 3,
    DRAFTING = 4,
    END = 5,
    PRELUDES = 6,

ACTION_OPTIONS: Dict[str, int] = {
    "Pass for this generation": 0,
    "End turn": 1,

}

AWARDS_INT_STR: Dict[int, str] = {
    0: "Miner",
    1: "Scientist",
    2: "Landlord",
    3: "Thermalist",
    4: "Banker",
}

MILESTONES_INT_STR: Dict[int, str] = {
    0: "Gardener",
    1: "Mayor",
    2: "Terraformer",
    3: "Planner",
    4: "Builder",
}

STANDARD_PROJECTS_INDEX_NAME: Dict[int, str] = {
    0: "Power Plant:SP",
    1: "Asteroid:SP",
    2: "Aquifer",
    3: "Greenery",
    4: "City"
}

PLAYERS_COLOR_ID: Dict[str, int] = {}

ACTION_OPTIONS_INT_STR: Dict[int, str] = {
    0: "Pass for this generation",
    1: "End turn",
}

CARD_NAMES_INT_STR: Dict[int, str] = {
    0: "karte1",
    1: "karte2",
    2: "karte3",
}

class ActionOptions(Enum):
    PASS_FOR_THIS_GENERATION = "Pass for this generation",
    END_TURN = "End turn",

class CustomEnv(gym.Env):
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    current_turn = None
    last_observation = None

    def __init__(self):
        super(CustomEnv, self).__init__()

        # # Eingabe in das Modell
        # # TODO das muss hier raus weil für das jeweilige modell ja immer man selbst dran ist bzw es keinen einfluss auf die aktion hat!
        # self.current_player = spaces.Discrete(NUMBER_PLAYERS) # welcher Spieler ist gerade dran
        # self.own_player_id = spaces.Discrete(NUMBER_OF_CARDS) # statt dem obendrüber damit die anderen spieler unterschieden werden können. sollte anhand der farbe bestimmt werden
        # self.current_phase = spaces.Discrete(len(PHASES.keys())) # initial_research, research, action, production, drafting, end
        # #self.initial_research_phase = spaces.MultiBinary(1) # ob wir in der research phase sind
        # self.dealt_project_cards = spaces.MultiBinary(NUMBER_OF_CARDS) # welche karten schon ausgespielt wurden
        # # initial research phase
        # self.available_corporations = spaces.MultiBinary(NUMBER_CORPORATIONS) # zwei davon sind immer 1
        # self.available_initial_project_cards = spaces.MultiBinary(NUMBER_OF_CARDS) # 10 davon sind 1
        # # action phase
        # self.available_actions = spaces.MultiBinary(len(ACTION_OPTIONS.keys())) # muss ich nochmal richtig zählen
        # self.select_action = spaces.Discrete(len(SELECTABLE_ACTIONS.keys())) # z.b. select card to remove 1 animals - und nochmal richtig zählen
        # self.cards_available_for_selection = spaces.MultiBinary(NUMBER_OF_CARDS) # nochmal zählen
        # self.min_energy_to_spend = spaces.Box(low=0, high=1, shape=(1,))
        # self.available_spaces = spaces.Discrete(len(ALL_SPACES)) # nochmal alle felder zählen
        # self.which_production = spaces.Discrete(5) # nochmal zählen
        # self.decrease_production_how_many_steps = spaces.Box(low=1, high=2, shape=(1,))
        # self.tile_to_place_name = spaces.Discrete(5) # Commercial District, Restricted Area, Natural Preserve, Nuclear Zone, Mohole Area,

        # Beobachtungsraum
        self.observation_space = spaces.Dict({
            AVAILABLE_ACTION_OPTIONS: MultiBinary(len(ACTION_OPTIONS_INT_STR.values())),
            SELECTED_ACTION_INDEX: Discrete(NUMBER_ALL_ACTIONS),
            AVAILABLE_CARDS: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_HEAT: Box(0, 500, (1,), np.int8),
            AVAILABLE_MC: Box(0, 500, (1,), np.int8),
            AVAILABLE_STEEL: Box(0, 500, (1,), np.int8),
            AVAILABLE_TITANIUM: Box(0, 500, (1,), np.int8),
            AVAILABLE_MICROBES: Box(0, 500, (1,), np.int8),
            STEEL_VALUE: Box(0, 3, (1,), np.int8),
            TITANIUM_VALUE: Box(0, 3, (1,), np.int8),
            RESERVE_HEAT: Box(0, 50, (1,), np.int8),
            RESERVE_MC: Box(0, 50, (1,), np.int8),
            RESERVE_STEEL: Box(0, 50, (1,), np.int8),
            RESERVE_TITANIUM: Box(0, 50, (1,), np.int8),
            AVAILABLE_SPACES: MultiBinary(NUMBER_SPACES),
            PLAYED_CARDS_ONE_HOT: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_MILESTONES: MultiBinary(NUMBER_OF_MILESTONES()),
            AVAILABLE_AWARDS: MultiBinary(NUMBER_OF_AWARDS()),
            AVAILABLE_STANDARD_PROJECTS: MultiBinary(NUMBER_OF_STANDARD_PROJECTS()),
        })

        self.action_space = spaces.Dict({
            SELECTED_ACTION_OPTION_INDEX: Discrete(NUMBER_ALL_ACTION_OPTIONS),
            SELECTED_CARD_INDEX: Discrete(NUMBER_OF_CARDS),
            PAY_HEAT_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MC_PERCENTAGE: Box(low=0, high=1, shape=(1,), dtype=np.float32),
            PAY_STEEL_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_TITANIUM_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MICROBES_PERCENTAGE: Box(0, 1, (1,), np.float32),
            MULTIPLE_SELECTED_CARDS: MultiBinary(NUMBER_OF_CARDS),
            SELECTED_SPACE_INDEX: Discrete(NUMBER_SPACES),
            SELECTED_PLAYER: Discrete(NUMBER_PLAYERS),
            SELECTED_CARD_FROM_PLAYED_CARDS_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_MILESTONE_INDEX: Discrete(NUMBER_OF_MILESTONES()),
            SELECTED_AWARD_INDEX: Discrete(NUMBER_OF_AWARDS()),
            SELECTED_STANDARD_PROJECT_INDEX: Discrete(NUMBER_OF_STANDARD_PROJECTS()),
        })

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        #self.http_connection = http.client.HTTPConnection("localhost", 8080)

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
                    "name": "Red",
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
        #self.http_connection.request("PUT", "/game", body=json_body)
        #response = self.http_connection.getresponse()
        #result = json.loads(response.read().decode())

        # self.player1 = Player(result["players"][0]["color"],
        #                       result["players"][0]["id"],
        #                       result["players"][0]["name"])
        # self.player2 = Player(result["players"][1]["color"],
        #                       result["players"][1]["id"],
        #                       result["players"][1]["name"])
        # self.player3 = Player(result["players"][2]["color"],
        #                       result["players"][2]["id"],
        #                       result["players"][2]["name"])

        return {
            "current_phase": self.current_phase.sample(),
            "dealt_project_cards": self.dealt_project_cards.sample(),
            "available_corporations": self.available_corporations.sample(),
            "available_initial_project_cards": self.available_initial_project_cards.sample(),
        }, {}

    def draft(self):
        return {
            "game": {
                "phase": "research"
            }
        }

    def normal_turn(self, action):

        # get_game(player.id, http_connection)
        current_state = {
            "waitingFor": {
                "title1": {
                    "message": "Select space for ${0} tile"
                },
                "title2": "Select space for ocean tile",
                "options": [
                    {
                        "title": "Standard projects"
                    },
                    {
                        "title": "Pass for this generation"
                    },
                    {
                        "title": {
                            "message": "Mollo"
                        }
                    },
                    {
                        "title": "Sell patents",
                        "cards": [
                            {
                                "name": "Testname1",
                                "calculatedCost": 15
                            }
                        ]
                    }
                ]
            },
            "thisPlayer": {
                "megaCredits": 15
            }
        }

        payload = None

        run_id = 894568394

        if "options" in current_state["waitingFor"]:
            available_options = current_state["waitingFor"]["options"]

            # TODO if index = standard project, check if is available and maybe choose other

            # die available options müssen noch von den namen her auf die korrekten indizes gemapped werden
            selected_option_from_all: str = ACTION_OPTIONS_INT_STR[action[SELECTED_ACTION_OPTION_INDEX]]
            selected_option_index = -1
            for idx, option in enumerate(available_options):
                if "message" in option["title"]:
                    name = option["title"]["message"]
                else:
                    name = option["title"]
                if name == selected_option_from_all:
                    selected_option_index = idx
                    break
            selected_option = available_options[selected_option_index]

            action_name = selected_option["title"]["message"] if "message" in selected_option["title"] else selected_option["title"]
            match action_name:
                case ("Pass for this generation",
                      "End Turn",
                      "Convert 8 heat into temperature",
                      "Convert 8 plants into greenery",
                      "Do nothing",
                      "Skip removal",
                      "Skip removing plants",
                      "Increase your plant production 1 step",
                      "Add a science resource to this card",
                      "Do not remove resource",
                      "Increase your energy production 2 steps",
                      "Increase titanium production 1 step",
                      "Increase megacredits production 1 step",
                      "Increase steel production 1 step",
                      "Increase plants production 1 step",
                      "Increase heat production 1 step",
                      "Increase energy production 1 step",
                      "Do not steal",
                      "Remove 2 microbes to raise oxygen level 1 step"
                      "Add 1 microbe to this card",
                      "Remove 3 microbes to increase your terraform rating 1 step",
                      "Don't place a greenery",
                      "Remove a science resource from this card to draw a card",
                      "Spend 1 steel to gain 7 M€.",
                      "Remove 2 microbes to raise temperature 1 step",
                      "Gain 4 plants",
                      "Spend 1 plant to gain 7 M€.",
                      "Gain plant",
                      "Gain 1 plant",
                      "Gain 3 plants",
                      "Gain 5 plants",
                      "Don't remove M€ from adjacent player",
                      "Take first action of ${0} corporation",
                      "Remove ${0} plants from ${1}",
                      "Remove ${0} ${1} from ${2}",
                      "Steal ${0} M€ from ${1}",
                      "Steal ${0} steel from ${1}",
                      "Add ${0} microbes to ${1}",
                      "Add resource to card ${0}",
                      "Add ${0} animals to ${1}",
                      "Fund ${0} award"):
                    payload = self.create_or_resp_option(run_id, selected_option_index)
                case "Play project card":
                    available_cards = selected_option["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_INDEX]]
                    selected_card = None
                    for card in available_cards:
                        if card["name"] == selected_card_from_all_name:
                            selected_card = card
                            break

                    card_cost = selected_card["calculatedCost"]
                    card_name = selected_card["name"]

                    payment_options = selected_option["paymentOptions"]
                    can_pay_with_heat = payment_options["heat"]
                    can_pay_with_steel = card_name in BUILDING_CARDS_SET # building cards
                    can_pay_with_titanium = card_name in SPACE_CARDS_SET # space cards
                    can_pay_with_microbes = False
                    if card_name in PLANT_CARDS_SET:
                        for p in current_state["players"]:
                            if p["color"] == player.color:
                                for card in p["tableau"]:
                                    if card["name"] == "Psychrophiles":
                                        can_pay_with_microbes = True
                                        break
                                break

                    pay_heat_percentage = action[PAY_HEAT_PERCENTAGE]
                    pay_mc_percentage = action[PAY_MC_PERCENTAGE]
                    pay_steel_percentage = action[PAY_STEEL_PERCENTAGE]
                    pay_titanium_percentage = action[PAY_TITANIUM_PERCENTAGE]
                    pay_microbes_percentage = action[PAY_MICROBES_PERCENTAGE]

                    available_heat = current_state["thisPlayer"]["heat"]
                    available_mc = current_state["thisPlayer"]["megaCredits"]
                    available_steel = current_state["thisPlayer"]["steel"]
                    steel_value = current_state["thisPlayer"]["steelValue"]
                    available_titanium = current_state["thisPlayer"]["titanium"]
                    titanium_value = current_state["thisPlayer"]["titaniumValue"]
                    available_microbes = current_state["waitingFor"]["microbes"]
                    microbes_value = 2

                    reserve_units = selected_card["reserveUnits"] if "reserveUnits" in selected_card else None
                    if reserve_units is not None:
                        available_heat -= reserve_units["heat"]
                        available_mc -= reserve_units["mc"]
                        available_titanium -= reserve_units["titanium"]
                        available_steel -= reserve_units["steel"]

                    pay_heat = math.floor(pay_heat_percentage * available_heat) * (1 if can_pay_with_heat else 0)
                    pay_mc = math.floor(pay_mc_percentage * available_mc)
                    pay_steel = math.floor(pay_steel_percentage * available_steel) * (1 if can_pay_with_steel else 0)
                    pay_titanium = math.floor(pay_titanium_percentage * available_titanium) * (1 if can_pay_with_titanium else 0)
                    pay_microbes = math.floor(pay_microbes_percentage * available_microbes) * (1 if can_pay_with_microbes else 0)

                    payment = pay_heat + pay_mc + pay_steel * steel_value + pay_titanium * titanium_value + pay_microbes * microbes_value

                    if payment != card_cost:
                        pay_heat = 0
                        pay_mc = 0
                        pay_steel = 0
                        pay_titanium = 0
                        pay_microbes = 0

                        available_payments = ["mc"]
                        if can_pay_with_heat: available_payments.append("heat")
                        if can_pay_with_steel: available_payments.append("steel")
                        if can_pay_with_titanium: available_payments.append("titanium")
                        if can_pay_with_microbes: available_payments.append("microbes")
                        random.shuffle(available_payments)  # random order

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
                                if available_microbes * microbes_value >= remaining_cost:
                                    pay_microbes = math.ceil(remaining_cost / microbes_value)
                                    break
                                else:
                                    pay_microbes = available_microbes
                                    remaining_cost = remaining_cost - available_microbes * microbes_value

                    payload = self.create_or_resp_project_card_payment(run_id, selected_option_index, card_name, pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes)
                case "Sell patents": # multiple cards
                    selected_cards = []
                    selected_card_indices = action[MULTIPLE_SELECTED_CARDS]
                    for idx, binary in enumerate(selected_card_indices):
                        if binary == 1:
                            selected_card_name: str = CARD_NAMES_INT_STR[idx]
                            selected_cards.append(selected_card_name)
                    payload = self.create_or_resp_card_cards(run_id, selected_option_index, selected_cards)
                case ("Perform an action from a played card", # single card
                      "Select a card to discard",
                      "Add 3 microbes to a card",
                      "Select card to add 2 microbes",
                      "Select card to remove 2 Animal(s)",
                      "Select card to add 2 animals",
                      "Select card to add 4 animals",
                      "Add 2 animals to a card"):
                    available_cards = selected_option["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_FROM_PLAYED_CARDS_INDEX]]
                    selected_card = None
                    for card in available_cards:
                        if card["name"] == selected_card_from_all_name:
                            selected_card = card
                            break
                    payload = self.create_or_resp_card_cards(run_id, selected_option_index, [selected_card["name"]])
                case ("Select space for greenery tile",
                      "Convert ${0} plants into greenery"):
                    available_spaces_ids = selected_option["spaces"]
                    selected_space_index = action[SELECTED_SPACE_INDEX]
                    selected_space_id = str(selected_space_index + 1) # TODO maybe "1" is not treated the same as "01"
                    payload = self.create_or_resp_space_space_id(run_id, selected_option_index, selected_space_id)
                case "Select adjacent player to remove 4 M€ from":
                    available_players_colors = selected_option["players"]
                    selected_player_color = action[SELECTED_PLAYER]
                    selected_player = None # TODO
                    payload = self.create_or_resp_player_player(run_id, selected_option_index, selected_player)
                case "Fund an award (${0} M€)":
                    available_awards = selected_option["options"]
                    selected_award_from_all_name: str = AWARDS_INT_STR[action[SELECTED_AWARD_INDEX]]
                    selected_award_index = -1
                    for idx, award in enumerate(available_awards):
                        if award["name"] == selected_award_from_all_name:
                            selected_award_index = idx
                            break
                    payload = self.create_or_resp_or_resp_option(run_id, selected_option_index, selected_award_index)
                case "Standard projects":
                    # possibly none are available
                    selected_standard_project_name = STANDARD_PROJECTS_INDEX_NAME[action[SELECTED_STANDARD_PROJECT_INDEX]]
                    self.create_or_resp_card_cards(run_id, selected_option_index, [selected_standard_project_name])
                case "Claim a milestone":
                    available_milestones = selected_option["options"]
                    selected_milestone_from_all_name: str = MILESTONES_INT_STR[action[SELECTED_MILESTONE_INDEX]]
                    selected_milestone_index = -1
                    for idx, milestone in enumerate(available_milestones):
                        if milestone["name"] == selected_milestone_from_all_name:
                            selected_milestone_index = idx
                            break
                    self.create_or_resp_or_resp_option(run_id, selected_option_index, selected_milestone_index)
        else:
            message = current_state["waitingFor"]["title"]["message"] if "message" in current_state["waitingFor"]["title"] else current_state["waitingFor"]["title"]
            match message:
                case ("Select space for ${0} tile",
                      "Select space for ocean tile",
                      "Select space reserved for ocean to place greenery tile",
                      "Select a space with a steel or titanium bonus",
                      "Select space adjacent to a city tile",
                      "Select place next to no other tile for city",
                      "Select space next to greenery for special tile",
                      "Select either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons",
                      "Select a space with a steel or titanium bonus adjacent to one of your tiles",
                      "Select space next to at least 2 other city tiles",
                      "Select a land space to place an ocean tile",
                      "Select space for city tile",
                      "Select space for greenery tile",
                      "Select space for ocean from temperature increase",
                      "Select space for claim",
                      "Select space for first ocean",
                      "Select space for second ocean",
                      "Select space for special city tile"):
                    selected_space = 0
                    payload = self.create_space_id_response(run_id, selected_space)
                case "Select player to decrease ${0} production by ${1} step(s)":
                    selected_player = 0
                    payload = self.create_player_response(run_id, selected_player)
                case ("Select card to add ${0} ${1}",
                      "Select builder card to copy",
                      "Select 1 card(s) to keep",
                      "Select card to remove 1 Microbe(s)",
                      "Select card to remove 1 Animal(s)",
                      "Select prelude card to play"):
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_card = None
                    self.create_cards_response(run_id, [selected_card["name"]])
                case "Select 2 card(s) to keep":
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_cards_names = []
                    self.create_cards_response(run_id, selected_cards_names)
                case "Select card(s) to buy":
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_cards_names = []
                    self.create_cards_response(run_id, selected_cards_names)
                case "You cannot afford any cards":
                    self.create_cards_response(run_id, [])
                case "Play project card":
                    pay_mc = 0
                    pay_heat = 0
                    pay_steel = 0
                    pay_titanium = 0
                    pay_microbes = 0
                    self.create_project_card_payment_response(run_id, "test", pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes)
                    pass
                case ("Select how to pay for the ${0} standard project",
                      "Select how to spend ${0} M€",
                      "Select how to spend ${0} M€ for ${1} cards",
                      "Select how to pay for ${0} action",
                      "Select how to pay for award",
                      "Select how to pay for action",
                      "Select how to pay for milestone"):
                    if message == "Select how to pay for the ${0} standard project":
                        pass
                    elif message == "Select how to spend ${0} M€":
                        pass
                    elif message == "Select how to spend ${0} M€ for ${1} cards":
                        pass
                    elif message == "Select how to pay for ${0} action":
                        pass
                    elif message == "Select how to pay for award":
                        pass


                    cost = current_state["waitingFor"]["cost"]
                    pay_mc = 0
                    pay_heat = 0
                    pay_steel = 0
                    pay_titanium = 0
                    payload = self.create_payment_response(run_id, pay_heat, pay_mc, pay_steel, pay_titanium)
                case ("Select amount of heat production to decrease",
                      "Select amount of energy to spend"):
                    amount = 0
                    min = current_state["waitingFor"]["min"]
                    max = current_state["waitingFor"]["max"]
                    payload = self.create_amount_response(run_id, amount)

        # send_player_input(json.dumps(select_space_data), player.id, http_connection)
        return {
            "game": {
                "phase": "action"
            }
        }

    def step(self, action):
        res = None
        match (self.last_observation["current_phase"]):
            case PhasesEnum.DRAFTING.value:
                res = self.draft()
            case PhasesEnum.ACTION.value, PhasesEnum.PRODUCTION.value, PhasesEnum.PRELUDES.value:
                res = self.normal_turn(action)

        # TODO herausfinden welcher player gerade dran ist, am besten als parameter
        # Beispiel-Logik für Belohnung und Fertigkeitsstatus
        reward = np.random.random()
        done = reward > 0.95

        next_phase = PhasesEnum.INITIAL_RESEARCH
        match (res["game"]["phase"]):
            case "research":
                next_phase = PhasesEnum.RESEARCH
            case "drafting":
                next_phase = PhasesEnum.DRAFTING

        current_phase_ordinal = next_phase.value
        observation = {
            "current_phase": current_phase_ordinal,
            "dealt_project_cards": self.dealt_project_cards.sample(),
            "available_corporations": self.available_corporations.sample(),
            "available_initial_project_cards": self.available_initial_project_cards.sample(),
        }

        return observation, reward, done, False, {}

    def create_or_resp_option(self, run_id, index):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "option"
            }
        }

    def create_or_resp_project_card_payment(self, run_id, index, card_name, heat, mc, steel, titanium, microbes):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "projectCard",
                "card": card_name,
                "payment": {
                    "heat":heat,
                    "megaCredits": mc,
                    "steel":steel,
                    "titanium":titanium,
                    "plants":0,
                    "microbes":microbes,
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

    def create_or_resp_card_cards(self, run_id, index, card_names):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "card",
                "cards": card_names
            }
        }

    def create_space_id_response(self, run_id, selected_space):
        return {
            "runId": run_id,
            "type": "space",
            "spaceId": selected_space
        }

    def create_or_resp_space_space_id(self, run_id, index, selected_space):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "space",
                "spaceId": selected_space
            }
        }

    def create_or_resp_player_player(self, run_id, index, selected_player):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "player",
                "player": selected_player
            }
        }

    def create_or_resp_or_resp_option(self, run_id, action_index, index2):
        return {
            "runId": run_id,
            "type": "or",
            "index": action_index,
            "response": {
                "type": "or",
                "index": index2,
                "response": {
                    "type": "option"
                }
            }
        }

    def create_player_response(self, run_id, selected_player):
        return {
            "runId": run_id,
            "type": "player",
            "player": selected_player
        }

    def create_cards_response(self, run_id, selected_cards_names):
        return {
            "runId": run_id,
            "type": "card",
            "cards": selected_cards_names
        }

    def create_payment_response(self, run_id, heat, mc, steel, titanium):
        return {
            "runId": run_id,
            "type": "payment",
            "payment": {
                "heat": heat,
                "megaCredits": mc,
                "steel": steel,
                "titanium": titanium,
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

    def create_amount_response(self, run_id, amount):
        return {
            "runId": run_id,
            "type": "amount",
            "amount": amount
        }

    def create_project_card_payment_response(self, run_id, card_name, heat, mc, steel, titanium, microbes):
        select_card_data = {
            "runId": run_id,
            "type": "projectCard",
            "card": card_name,
            "payment": {
                "heat": heat,
                "megaCredits": mc,
                "steel": steel,
                "titanium": titanium,
                "plants": 0,
                "microbes": microbes,
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
