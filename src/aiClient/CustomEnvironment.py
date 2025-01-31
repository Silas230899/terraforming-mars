import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import http.client
import json
import random

from AiPlayer import Player

NUMBER_CORPORATIONS = 12

NUMBER_PLAYERS = 3

NUMBER_OF_CARDS = 170

PHASES = {
    0: "INITIAL_RESEARCH",
    1: "RESEARCH",
    2: "ACTION",
    3: "PRODUCTION",
    4: "DRAFTING",
    5: "END"
}

ACTION_OPTIONS = {
    0: "Pass for this generation",
    1: "Play project card",
    2: "Standard project"
}

SELECTABLE_ACTIONS = {
    0: "Select space for ${0} tile",
    1: "Select player to decrease ${0} production by ${1} step(s)"
}

ALL_SPACES = [1,2,3,4,5]

class CustomEnv(gym.Env):
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    current_turn = None

    def __init__(self):
        super(CustomEnv, self).__init__()

        # Eingabe in das Modell
        self.current_player = spaces.Discrete(NUMBER_PLAYERS) # welcher Spieler ist gerade dran
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



        # Ausgabe des Modells
        # research phase
        self.chosen_corporation = spaces.Discrete(NUMBER_CORPORATIONS) # ein einziges wählen
        self.chosen_initial_project_cards = spaces.Box(0, 1, shape=(NUMBER_OF_CARDS,), dtype=np.float32) # select 10
        # action phase
        self.chose_action = spaces.Discrete(len(ACTION_OPTIONS.keys())) # eine der verfügbaren aktionen wählen
        self.selected_card = spaces.Box(0, 1, shape=(NUMBER_OF_CARDS,), dtype=np.float32) # select 1
        self.select_how_many = spaces.MultiBinary(1) # wenn 0 oder 1 gezogen werden müssen
        self.selected_space = spaces.Discrete(len(ALL_SPACES)) #richtig zählen
        self.selected_player = spaces.Discrete(NUMBER_PLAYERS)


        # Diskreter Beobachtungsraum
        self.discrete_obs_space = spaces.Discrete(10)
        # Kontinuierlicher Beobachtungsraum
        self.continuous_obs_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        # Kombination von Beobachtungen
        self.observation_space = spaces.Dict({
            "discrete": self.current_player,
            "continuous": self.continuous_obs_space
        })

        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

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

        discrete_obs = self.current_player.sample()
        continuous_obs = self.continuous_obs_space.sample()
        return {"discrete": discrete_obs, "continuous": continuous_obs}, {}

    def step(self, action):
        # Beispiel-Logik für Belohnung und Fertigkeitsstatus
        reward = np.random.random()
        done = reward > 0.95
        if action == 4:
            print(4)
        else:
            print("not 4")
        #    self.discrete_obs_space = np.int64(3)

        # discrete_obs = self.discrete_obs_space.sample()
        discrete_obs = self.current_player.sample()
        continuous_obs = self.continuous_obs_space.sample()
        observation = {"discrete": discrete_obs, "continuous": continuous_obs}

        return observation, reward, done, False, {}
