from enum import Enum
from typing import Dict

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import json
import random

NUMBER_CORPORATIONS = 12
NUMBER_PLAYERS = 3

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

CARD_NAMES: Dict[str, int] = {

}

class ActionOptions(Enum):
    PASS_FOR_THIS_GENERATION = "Pass for this generation",
    END_TURN = "End turn",

class ActionSpaceRanges(Enum):
    TEST = range(-5, -1),
    WAITING_FOR_OPTIONS = range(0, 58),
    CARD_SELECTION = range(58, 58 + 195), # number of cards = 195
    PAY_MC_PERCENTAGE = range(195 + 58, 195 + 58 + 1)

class CustomEnv(gym.Env):
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    current_turn = None
    last_observation = None

    def __init__(self):
        super(CustomEnv, self).__init__()

        # Eingabe in das Modell
        # TODO das muss hier raus weil für das jeweilige modell ja immer man selbst dran ist bzw es keinen einfluss auf die aktion hat!
        self.current_player = spaces.Discrete(NUMBER_PLAYERS) # welcher Spieler ist gerade dran
        self.own_player_id = spaces.Discrete(NUMBER_OF_CARDS) # statt dem obendrüber damit die anderen spieler unterschieden werden können. sollte anhand der farbe bestimmt werden
        self.current_phase = spaces.Discrete(len(PHASES.keys())) # initial_research, research, action, production, drafting, end
        #self.initial_research_phase = spaces.MultiBinary(1) # ob wir in der research phase sind
        self.dealt_project_cards = spaces.MultiBinary(NUMBER_OF_CARDS) # welche karten schon ausgespielt wurden
        # initial research phase
        self.available_corporations = spaces.MultiBinary(NUMBER_CORPORATIONS) # zwei davon sind immer 1
        self.available_initial_project_cards = spaces.MultiBinary(NUMBER_OF_CARDS) # 10 davon sind 1
        # action phase
        self.available_actions = spaces.MultiBinary(len(ACTION_OPTIONS.keys())) # muss ich nochmal richtig zählen
        self.select_action = spaces.Discrete(len(SELECTABLE_ACTIONS.keys())) # z.b. select card to remove 1 animals - und nochmal richtig zählen
        self.cards_available_for_selection = spaces.MultiBinary(NUMBER_OF_CARDS) # nochmal zählen
        self.min_energy_to_spend = spaces.Box(low=0, high=1, shape=(1,))
        self.available_spaces = spaces.Discrete(len(ALL_SPACES)) # nochmal alle felder zählen
        self.which_production = spaces.Discrete(5) # nochmal zählen
        self.decrease_production_how_many_steps = spaces.Box(low=1, high=2, shape=(1,))
        self.tile_to_place_name = spaces.Discrete(5) # Commercial District, Restricted Area, Natural Preserve, Nuclear Zone, Mohole Area,

        # Beobachtungsraum
        self.observation_space = spaces.Dict({
            "current_phase": self.current_phase,
            "dealt_project_cards": self.dealt_project_cards,
            "available_corporations": self.available_corporations,
            "available_initial_project_cards": self.available_initial_project_cards,
        })

        self.action_space = spaces.Tuple((
            gym.spaces.Discrete(3),
            gym.spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),
        ))

        # Aktionsraum
        self.action_space = spaces.Box(low=0, high=1.0, shape=(4,), dtype=np.float32)

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

    def action_option_argmax(self, all_options_percentages, available_options):
        return max(list(map(lambda name: all_options_percentages[ACTION_OPTIONS[name]], available_options)), key=lambda i: all_options_percentages[i])

    def card_selection_argmax(self, all_cards_percentages, available_options):
        return max(list(map(lambda name: all_cards_percentages[CARD_NAMES[name]], available_options)), key=lambda i: all_cards_percentages[i])

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
            #index = np.argmax(action[ActionSpaceRanges.WAITING_FOR_OPTIONS])
            option_percentages = action[ActionSpaceRanges.WAITING_FOR_OPTIONS]
            # hier mappt jeder index immer auf dieselbe option
            available_options = current_state["waitingFor"]["options"]
            # die available options müssen noch von den namen her auf die korrekten indizes gemapped werden
            # choose from the available_options the one with the highest percentage in option_percentages
            # TODO if index = standard project, check if is available and maybe choose other
            selected_option_index = self.action_option_argmax(
                all_options_percentages=action[ActionSpaceRanges.WAITING_FOR_OPTIONS],
                available_options=current_state["waitingFor"]["options"])
            option = current_state["waitingFor"]["options"][selected_option_index]
            action_name = option["title"]["message"] if "message" in option["title"] else option["title"]
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
                    playable_cards = option["cards"]
                    selected_card = self.card_selection_argmax(
                        all_cards_percentages=action[ActionSpaceRanges.CARD_SELECTION],
                        available_options=playable_cards)
                    card_cost = selected_card["calculatedCost"]
                    card_name = selected_card["name"]

                    pay_mc_percentage = action[ActionSpaceRanges.PAY_MC_PERCENTAGE]
                    pay_steel_percentage = action[12]
                    available_mc = current_state["thisPlayer"]["megaCredits"]
                    available_steel = current_state["thisPlayer"]["steel"]
                    steel_value = current_state["thisPlayer"]["steelValue"]
                    pay_mc = pay_mc_percentage * available_mc # aktivierungsfunktion
                    pay_steel = pay_steel_percentage * available_steel
                    if pay_mc + pay_steel * steel_value != card_cost:
                        pass
                    payload = self.create_or_resp_project_card_payment(run_id, selected_option_index, card_name, 0, 0, 0, 0)
                case "Standard project":
                    pass
                case "Sell patents": # multiple cards
                    playable_cards = option["cards"]
                    # TODO maybe choose all above 50 %
                    selected_cards = []
                    payload = self.create_or_resp_card_cards(run_id, selected_option_index, selected_cards)
                case ("Perform an action from a played card", # single card
                      "Select a card to discard",
                      "Add 3 microbes to a card",
                      "Select card to add 2 microbes",
                      "Select card to remove 2 Animal(s)",
                      "Select card to add 2 animals",
                      "Select card to add 4 animals",
                      "Add 2 animals to a card"):
                    playable_cards = option["cards"]
                    selected_card = None
                    payload = self.create_or_resp_card_cards(run_id, selected_option_index, [selected_card["name"]])
                case "Claim a milestone":
                    pass
                case ("Select space for greenery tile",
                      "Convert ${0} plants into greenery"):
                    available_spaces = option["spaces"]
                    selected_space = 0
                    payload = self.create_or_resp_space_space_id(run_id, selected_option_index, selected_space)
                case "Select adjacent player to remove 4 M€ from":
                    available_players = option["players"]
                    selected_player = 0
                    payload = self.create_or_resp_player_player(run_id, selected_option_index, selected_player)
                    pass
                case "Fund an award (${0} M€)":
                    payload = self.create_or_resp_or_resp_option(run_id, selected_option_index, 0)
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
