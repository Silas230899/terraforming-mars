import math
from enum import Enum
from typing import Dict

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import json
import random

from gymnasium.spaces import Box, Discrete, MultiBinary
from numpy import argmax

import ppo
from Player import Player
from action_observation_names import *

BUILDING_CARDS_SET = {'Smelting Plant', 'SF Memorial', 'Self-Sufficient Settlement', 'Polar Industries', 'Mohole Excavation', 'Mohole', 'Mining Operations', 'Martian Industries', 'Lava Tube Settlement', 'House Printing', 'Early Settlement', 'Dome Farming', 'Cheung Shing MARS', 'AI Central', 'Aquifer Pumping', 'Artificial Lake', 'Biomass Combustors', 'Building Industries', 'Capital', 'Carbonate Processing', 'Colonizer Training Camp', 'Commercial District', 'Corporate Stronghold', 'Cupola City', 'Deep Well Heating', 'Development Center', 'Domed Crater', 'Electro Catapult', 'Eos Chasma National Park', 'Equatorial Magnetizer', 'Food Factory', 'Fueled Generators', 'Fuel Factory', 'Fusion Power', 'Geothermal Power', 'GHG Factories', 'Great Dam', 'Greenhouses', 'Heat Trappers', 'Immigrant City', 'Industrial Center', 'Industrial Microbes', 'Ironworks', 'Magnetic Field Dome', 'Magnetic Field Generators', 'Mars University', 'Martian Rails', 'Medical Lab', 'Mine', 'Mining Area', 'Mining Rights', 'Mining Rights', 'Mining Rights', 'Mohole Area', 'Natural Preserve', 'Noctis City', 'Noctis Farming', 'Nuclear Power', 'Olympus Conference', 'Open City', 'Ore Processor', 'Peroxide Power', 'Physics Complex', 'Power Infrastructure', 'Power Plant', 'Protected Valley', 'Rad-Chem Factory', 'Research Outpost', 'Rover Construction', 'Soil Factory', 'Solar Power', 'Space Elevator', 'Steelworks', 'Strip Mine', 'Tectonic Stress Power', 'Titanium Mine', 'Tropical Resort', 'Underground City', 'Underground Detonations', 'Urbanized Area', 'Water Splitting Plant', 'Windmills'}

SPACE_CARDS_SET = {'Space Hotels', 'Point Luna', 'Orbital Construction Yard', 'Space Elevator', 'Aerobraked Ammonia Asteroid', 'Asteroid', 'Asteroid Mining', 'Beam From A Thorium Asteroid', 'Big Asteroid', 'Callisto Penal Mines', 'Comet', 'Convoy From Europa', 'Deimos Down', 'Ganymede Colony', 'Giant Ice Asteroid', 'Giant Space Mirror', 'Ice Asteroid', 'Immigration Shuttles', 'Imported GHG', 'Imported Hydrogen', 'Imported Nitrogen', 'Import of Advanced GHG', 'Interstellar Colony Ship', 'Io Mining Industries', 'Lagrange Observatory', 'Large Convoy', 'Methane From Titan', 'Miranda Resort', 'Nitrogen-Rich Asteroid', 'Optimal Aerobraking', 'Phobos Space Haven', 'Satellites', 'Security Fleet', 'Shuttles', 'Solar Wind Power', 'Soletta', 'Space Mirrors', 'Space Station', 'Technology Demonstration', 'Terraforming Ganymede', 'Toll Station', 'Towing A Comet', 'Trans-Neptune Probe', 'Vesta Shipyard', 'Water Import From Europa'}

PLANT_CARDS_SET = {'Biosphere Support', 'Dome Farming', 'Ecology Experts', 'Experimental Forest', 'Adapted Lichen', 'Advanced Ecosystems', 'Algae', 'Arctic Algae', 'Bushes', 'Ecological Zone', 'Eos Chasma National Park', 'Farming', 'Grass', 'Greenhouses', 'Heather', 'Kelp Farming', 'Lichen', 'Mangrove', 'Moss', 'Nitrophilic Moss', 'Noctis Farming', 'Plantation', 'Protected Valley', 'Trees', 'Tundra Farming'}

NUMBER_CORPORATIONS = 12
NUMBER_PLAYERS = 3
# NUMBER_OF_CARDS = 211 + 2 + 6 + 50 + 14 # 283
def NUMBER_OF_CARDS(): return len(CARD_NAMES_INT_STR.values())
NUMBER_ALL_ACTION_OPTIONS = 57
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

PLAYERS_ID_COLOR: Dict[int, str] = {
    0: "red",
    1: "green",
    2: "yellow"
}

ACTION_OPTIONS_INDEX_NAME: Dict[int, str] = {
    0: "Pass for this generation",
    1: "End turn",
    2: "Convert 8 heat into temperature",
    3: "Convert 8 plants into greenery",
    4: "Do nothing",
    5: "Skip removal",
    6: "Skip removing plants",
    7: "Increase your plant production 1 step",
    8: "Add a science resource to this card",
    9: "Do not remove resource",
    10: "Increase your energy production 2 steps",
    11: "Increase titanium production 1 step",
    12: "Increase megacredits production 1 step",
    13: "Increase steel production 1 step",
    14: "Increase plants production 1 step",
    15: "Increase heat production 1 step",
    16: "Increase energy production 1 step",
    17: "Do not steal",
    18: "Remove 2 microbes to raise oxygen level 1 step",
    19: "Add 1 microbe to this card",
    20: "Remove 3 microbes to increase your terraform rating 1 step",
    21: "Don't place a greenery",
    22: "Remove a science resource from this card to draw a card",
    23: "Spend 1 steel to gain 7 M€.",
    24: "Remove 2 microbes to raise temperature 1 step",
    25: "Gain 4 plants",
    26: "Spend 1 plant to gain 7 M€.",
    27: "Gain plant",
    28: "Gain 1 plant",
    29: "Gain 3 plants",
    30: "Gain 5 plants",
    31: "Don't remove M€ from adjacent player",
    32: "Take first action of ${0} corporation",
    33: "Remove ${0} plants from ${1}",
    34: "Remove ${0} ${1} from ${2}",
    35: "Steal ${0} M€ from ${1}",
    36: "Steal ${0} steel from ${1}",
    37: "Add ${0} microbes to ${1}",
    38: "Add resource to card ${0}",
    39: "Add ${0} animals to ${1}",
    40: "Fund ${0} award",
    41: "Play project card",
    42: "Sell patents",
    43: "Perform an action from a played card",
    44: "Select a card to discard",
    45: "Add 3 microbes to a card",
    46: "Select card to add 2 microbes",
    47: "Select card to remove 2 Animal(s)",
    48: "Select card to add 2 animals",
    49: "Select card to add 4 animals",
    50: "Add 2 animals to a card",
    51: "Select space for greenery tile",
    52: "Convert ${0} plants into greenery",
    53: "Select adjacent player to remove 4 M€ from",
    54: "Fund an award (${0} M€)",
    55: "Standard projects",
    56: "Claim a milestone",
}

CARD_NAMES_INT_STR: Dict[int, str] = {
0: "Sell Patents",
1: "Power Plant:SP",
2: "Asteroid:SP",
3: "Buffer Gas",
4: "Aquifer",
5: "Greenery",
6: "City",
7: "Convert Plants",
8: "Convert Heat",
9: "Acquired Company",
10: "Adaptation Technology",
11: "Adapted Lichen",
12: "Advanced Alloys",
13: "Advanced Ecosystems",
14: "Aerobraked Ammonia Asteroid",
15: "AI Central",
16: "Air Raid",
17: "Algae",
18: "Anti-Gravity Technology",
19: "Ants",
20: "Aquifer Pumping",
21: "Aquifer Turbines",
22: "ArchaeBacteria", # TODO maybe a bug
23: "Artificial Lake",
24: "Artificial Photosynthesis",
25: "Arctic Algae",
26: "Asteroid",
27: "Asteroid Mining",
28: "Asteroid Mining Consortium",
29: "Breathing Filters",
30: "Bribed Committee",
31: "Beam From A Thorium Asteroid",
32: "Big Asteroid",
33: "Biomass Combustors",
34: "Birds",
35: "Black Polar Dust",
36: "Building Industries",
37: "Bushes",
38: "Business Contacts",
39: "Business Network",
40: "Callisto Penal Mines",
41: "Carbonate Processing",
42: "Capital",
43: "Caretaker Contract",
44: "Cartel",
45: "CEO's Favorite Project",
46: "Cloud Seeding",
47: "Colonizer Training Camp",
48: "Comet",
49: "Commercial District",
50: "Convoy From Europa",
51: "Corporate Stronghold",
52: "Cupola City",
53: "Decomposers",
54: "Deep Well Heating",
55: "Deimos Down",
56: "Designed Microorganisms",
57: "Development Center",
58: "Dirigibles",
59: "Dome Farming",
60: "Domed Crater",
61: "Dust Seals",
62: "Early Settlement",
63: "Earth Catapult",
64: "Earth Office",
65: "Eccentric Sponsor",
66: "Ecological Zone",
67: "Ecology Experts",
68: "Electro Catapult",
69: "Energy Saving",
70: "Energy Tapping",
71: "Eos Chasma National Park",
72: "Equatorial Magnetizer",
73: "Extreme-Cold Fungus",
74: "Farming",
75: "Fish",
76: "Flooding",
77: "Food Factory",
78: "Fuel Factory",
79: "Fueled Generators",
80: "Fusion Power",
81: "Ganymede Colony",
82: "Gene Repair",
83: "Geothermal Power",
84: "GHG Producing Bacteria",
85: "GHG Factories",
86: "Giant Ice Asteroid",
87: "Giant Space Mirror",
88: "Grass",
89: "Great Aquifer",
90: "Great Dam",
91: "Great Escarpment Consortium",
92: "Greenhouses",
93: "Gyropolis",
94: "Hackers",
95: "Heather",
96: "Heat Trappers",
97: "Herbivores",
98: "Hired Raiders",
99: "House Printing",
100: "Ice Asteroid",
101: "Ice Cap Melting",
102: "Immigrant City",
103: "Immigration Shuttles",
104: "Imported GHG",
105: "Imported Hydrogen",
106: "Imported Nitrogen",
107: "Import of Advanced GHG",
108: "Indentured Workers",
109: "Industrial Microbes",
110: "Insects",
111: "Insulation",
112: "Interstellar Colony Ship",
113: "Invention Contest",
114: "Inventors' Guild",
115: "Investment Loan",
116: "Io Mining Industries",
117: "Ironworks",
118: "Kelp Farming",
119: "Lagrange Observatory",
120: "Lake Marineris",
121: "Land Claim",
122: "Large Convoy",
123: "Lava Flows",
124: "Lava Tube Settlement",
125: "Lichen",
126: "Lightning Harvest",
127: "Livestock",
128: "Local Heat Trapping",
129: "Lunar Beam",
130: "Magnetic Field Dome",
131: "Magnetic Field Generators",
132: "Martian Industries",
133: "Mangrove",
134: "Mars University",
135: "Martian Rails",
136: "Mass Converter",
137: "Media Archives",
138: "Media Group",
139: "Medical Lab",
140: "Methane From Titan",
141: "Micro-Mills",
142: "Mine",
143: "Mineral Deposit",
144: "Miranda Resort",
145: "Mining Area",
146: "Mining Expedition",
147: "Mining Operations",
148: "Mining Quota",
149: "Mining Rights",
150: "Mohole",
151: "Mohole Area",
152: "Mohole Excavation",
153: "Moss",
154: "Natural Preserve",
155: "Nitrite Reducing Bacteria",
156: "Nitrogen-Rich Asteroid",
157: "Nitrophilic Moss",
158: "Noctis City",
159: "Noctis Farming",
160: "Nuclear Power",
161: "Nuclear Zone",
162: "Olympus Conference",
163: "Omnicourt",
164: "Open City",
165: "Optimal Aerobraking",
166: "Ore Processor",
167: "Permafrost Extraction",
168: "Peroxide Power",
169: "Pets",
170: "Phobos Space Haven",
171: "Physics Complex",
172: "Plantation",
173: "Polar Industries",
174: "Power Grid",
175: "Power Infrastructure",
176: "Power Plant",
177: "Power Supply Consortium",
178: "Predators",
179: "Protected Habitats",
180: "Protected Valley",
181: "Psychrophiles",
182: "Quantum Extractor",
183: "Rad-Chem Factory",
184: "Rad-Suits",
185: "Regolith Eaters",
186: "Release of Inert Gases",
187: "Research",
188: "Research Outpost",
189: "Restricted Area",
190: "Robotic Workforce",
191: "Rover Construction",
192: "Sabotage",
193: "Satellites",
194: "Search For Life",
195: "Security Fleet",
196: "Self-Sufficient Settlement",
197: "Sister Planet Support",
198: "Small Animals",
199: "Soil Factory",
200: "Solar Power",
201: "Solarnet",
202: "Space Elevator",
203: "Strip Mine",
204: "Subterranean Reservoir",
205: "Shuttles",
206: "Solar Wind Power",
207: "Soletta",
208: "Space Mirrors",
209: "Space Station",
210: "Special Design",
211: "Sponsors",
212: "Steelworks",
213: "Standard Technology",
214: "Symbiotic Fungus",
215: "Tardigrades",
216: "Technology Demonstration",
217: "Tectonic Stress Power",
218: "Terraforming Ganymede",
219: "Titanium Mine",
220: "Toll Station",
221: "Towing A Comet",
222: "Trans-Neptune Probe",
223: "Trees",
224: "Tropical Resort",
225: "Tundra Farming",
226: "Underground City",
227: "Underground Detonations",
228: "Urbanized Area",
229: "Vesta Shipyard",
230: "Viral Enhancers",
231: "Virus",
232: "Water Import From Europa",
233: "Water Splitting Plant",
234: "Wave Power",
235: "Windmills",
236: "Worms",
237: "Zeppelins",
238: "Beginner Corporation",
239: "CrediCor",
240: "EcoLine",
241: "Helion",
242: "Interplanetary Cinematics",
243: "Inventrix",
244: "Mining Guild",
245: "PhoboLog",
246: "Saturn Systems",
247: "Teractor",
248: "Tharsis Republic",
249: "Thorgate",
250: "United Nations Mars Initiative",
251: "Acquired Space Agency",
252: "Allied Bank",
253: "Biofuels",
254: "Biolab",
255: "Biosphere Support",
256: "Business Empire",
257: "Cheung Shing MARS",
258: "Donation",
259: "Experimental Forest",
260: "Galilean Mining",
261: "Huge Asteroid",
262: "Io Research Outpost",
263: "Loan",
264: "Martian Survey",
265: "Metal-Rich Asteroid",
266: "Metals Company",
267: "Nitrogen Shipment",
268: "Orbital Construction Yard",
269: "Point Luna",
270: "Power Generation",
271: "Research Coordination",
272: "Research Network",
273: "Robinson Industries",
274: "SF Memorial",
275: "Smelting Plant",
276: "Society Support",
277: "Space Hotels",
278: "Supplier",
279: "Supply Drop",
280: "UNMI Contractor",
281: "Valley Trust",
282: "Vitor",
283: "Arcadian Communities",
284: "Astrodrill",
285: "Advertising",
286: "Pharmacy Union",
287: "Industrial Center",
288: "Factorum",
289: "Lakefront Resorts",
290: "Mons Insurance",
291: "Splice",
292: "Philares",
293: "Recyclon",
294: "Manutech",
295: "Self-replicating Robots",
296: "Polyphemos",
297: "Penguins",
298: "Small Asteroid",
299: "Snow Algae"
}

TILE_NAMES_OF_SELECTABLE_SPACES: Dict[str, int] = {
    "Mohole Area": 0,
    "Nuclear Zone": 1,
    "Commercial District": 2,
    "Restricted Area": 3,
    "Natural Preserve": 4
}
NUMBER_OF_TILES_TO_SELECT_SPACE_FOR = 5

CORPORATIONS_WITH_FIRST_ACTION: Dict[str, int] = {
    "Valley Trust": 0,
    "Inventrix": 1,
    "Vitor": 2,
    "Tharsis Republic": 3,
}
NUMBER_OF_CORPORATIONS_WITH_FIRST_ACTION = 4

REMOVABLE_RESOURCES_NAMES = {
    "M€": 0,
    "steel": 1,
    "titanium": 2,
}
NUMBER_OF_REMOVABLE_RESOURCES = 3

DECREASABLE_PRODUCTIONS_NAMES = {
    "megacredits": 0,
    "steel": 1,
    "titanium": 2,
    "heat": 3,
    "plants": 4,
    "energy": 5
}
NUMBER_OF_DECREASABLE_PRODUCTIONS = 6

CARDS_MICROBES_CAN_BE_ADDED_TO = {
    "Psychrophiles": 0,
    "GHG Producing Bacteria": 1,
    "Nitrite Reducing Bacteria": 2,
    "Tardigrades": 3,
    "Ants": 4,
    "Decomposers": 5,
}
NUMBER_OF_CARDS_MICROBES_CAN_BE_ADDED_TO = 6

CARDS_RESOURCES_CAN_BE_ADDED_TO = {
    "Regolith Eaters": 0,
    "Tardigrades": 1,
    "GHG Producing Bacteria": 2,
    "Ecological Zone": 3,
    "Pets": 4,
    "Decomposers": 5,
} # unused

ALL_CORPORATIONS_INDEX_NAME = {
    0: "CrediCor",
    1: "EcoLine",
    2: "Helion",
    3: "Interplanetary Cinematics",
    4: "Inventrix",
    5: "Mining Guild",
    6: "PhoboLog",
    7: "Tharsis Republic",
    8: "Thorgate",
    9: "United Nations Mars Initiative",
    10: "Saturn Systems",
    11: "Teractor",
    12: "Cheung Shing MARS",
    13: "Point Luna",
    14: "Robinson Industries",
    15: "Valley Trust",
    16: "Vitor",
}
CORPORATIONS_STARTING_MC = {
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
NUMBER_OF_CORPORATIONS = 17


class CustomEnv(gym.Env):
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    player_on_turn = None
    observed_player = None

    current_turn = None
    last_observation = None

    run_id = -1

    policy_model: ppo.PPO

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
            AVAILABLE_ACTION_OPTIONS: MultiBinary(NUMBER_ALL_ACTION_OPTIONS),
            SELECTED_ACTION_INDEX: Discrete(NUMBER_ALL_ACTIONS),
            AVAILABLE_CARDS: MultiBinary(NUMBER_OF_CARDS()),
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
            AVAILABLE_PLAYERS: MultiBinary(NUMBER_PLAYERS),
            MULTIPLE_PLAYED_CARDS: MultiBinary(NUMBER_OF_CARDS()),
            AVAILABLE_MILESTONES: MultiBinary(NUMBER_OF_MILESTONES()),
            AVAILABLE_AWARDS: MultiBinary(NUMBER_OF_AWARDS()),
            AVAILABLE_STANDARD_PROJECTS: MultiBinary(NUMBER_OF_STANDARD_PROJECTS()),

            # for "Take first action of ${0} corporation"
            CORPORATION_TO_TAKE_FIRST_ACTION_OF: Discrete(NUMBER_OF_CORPORATIONS_WITH_FIRST_ACTION),

            # "Remove ${0} plants from ${1}"
            AMOUNT_OF_PLANTS_TO_REMOVE: Box(0, 8, (1,), np.int8),
            PLAYER_TO_REMOVE_PLANTS_FROM: Discrete(NUMBER_PLAYERS),

            # "Remove ${0} ${1} from ${2}"
            RESOURCE_TO_REMOVE: Discrete(NUMBER_OF_REMOVABLE_RESOURCES),
            AMOUNT_OF_RESOURCE_TO_REMOVE: Box(0, 8, (1,), np.int8),
            PLAYER_TO_REMOVE_RESOURCE_FROM: Discrete(NUMBER_PLAYERS),

            # "Steal ${0} M€ from ${1}"
            AMOUNT_OF_MC_TO_STEAL: Box(0, 100, (1,), np.int8),
            PLAYER_TO_STEAL_MC_FROM: Discrete(NUMBER_PLAYERS),

            # "Steal ${0} steel from ${1}"
            AMOUNT_OF_STEEL_TO_STEAL: Box(0, 2, (1,), np.int8),
            PLAYER_TO_STEAL_STEEL_FROM: Discrete(NUMBER_PLAYERS),

            # "Add ${0} microbes to ${1}"
            AMOUNT_OF_MICROBES_TO_ADD: Box(0, 3, (1,), np.int8),
            CARD_TO_ADD_MICROBES_TO: Discrete(NUMBER_OF_CARDS_MICROBES_CAN_BE_ADDED_TO),

            # "Fund ${0} award"
            WHAT_AWARD_TO_FUND: Discrete(NUMBER_OF_AWARDS()),

            # Convert ${0} plants into greenery
            HOW_MANY_PLANTS_TO_CONVERT_INTO_GREENERY: Box(7, 8, (1,), np.int8),

            # Fund an award (${0} M€)
            FUND_AWARD_COST: Discrete(3), # 8, 14, 20

            # Select space for ${0} tile
            TILE_TO_SELECT_SPACE_FOR: Discrete(NUMBER_OF_TILES_TO_SELECT_SPACE_FOR),

            # Select player to decrease ${0} production by ${1} step(s)
            PRODUCTION_TO_DECREASE: Discrete(NUMBER_OF_DECREASABLE_PRODUCTIONS),
            STEPS_TO_DECREASE_PRODUCTION: Box(0, 8, (1,), np.int8),

            # Select how to pay for the ${0} standard project
            WHAT_STANDARD_PROJECT_TO_SELECT_HOW_TO_PAY_FOR: Discrete(NUMBER_OF_STANDARD_PROJECTS()),

            # Select amount of heat production to decrease
            MAX_AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE: Box(0, 50, (1,), np.int8),

            # Select amount of energy to spend
            MAX_AMOUNT_OF_ENERGY_TO_SPEND: Box(0, 50, (1,), np.int8),

            # Select a card to keep and pass the rest to ${0}
            PASS_REMAINING_DRAFT_CARDS_TO_WHOM: Discrete(NUMBER_PLAYERS),

            # Initial Research Phase
            AVAILABLE_CORPORATIONS: Discrete(NUMBER_OF_CORPORATIONS),
        })

        self.action_space = spaces.Dict({
            SELECTED_ACTION_OPTION_INDEX: Discrete(NUMBER_ALL_ACTION_OPTIONS),
            SELECTED_CARD_INDEX: Discrete(NUMBER_OF_CARDS()),
            PAY_HEAT_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MC_PERCENTAGE: Box(low=0, high=1, shape=(1,), dtype=np.float32),
            PAY_STEEL_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_TITANIUM_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MICROBES_PERCENTAGE: Box(0, 1, (1,), np.float32),
            MULTIPLE_SELECTED_CARDS: MultiBinary(NUMBER_OF_CARDS()),
            SELECTED_SPACE_INDEX: Discrete(NUMBER_SPACES),
            SELECTED_PLAYER: Discrete(NUMBER_PLAYERS),
            SELECTED_CARD_FROM_PLAYED_CARDS_INDEX: Discrete(NUMBER_OF_CARDS()),
            SELECTED_MILESTONE_INDEX: Discrete(NUMBER_OF_MILESTONES()),
            SELECTED_AWARD_INDEX: Discrete(NUMBER_OF_AWARDS()),
            SELECTED_STANDARD_PROJECT_INDEX: Discrete(NUMBER_OF_STANDARD_PROJECTS()),

            # Select 2 card(s) to keep
            TWO_SELECTED_CARDS_INDICES: MultiBinary(NUMBER_OF_CARDS()),

            # Select amount of heat production to decrease
            AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE: Box(0, 50, (1,), np.int8),

            # Select amount of energy to spend
            AMOUNT_OF_ENERGY_TO_SPEND: Box(0, 50, (1,), np.int8),

            # Select card(s) to buy
            MULTIPLE_SELECTED_RESEARCH_CARDS: MultiBinary(NUMBER_OF_CARDS()),
            DONT_BUY_CARD: Discrete(2), # zero means no, one means yes

            # Initial Research Phase
            SELECTED_CORPORATION: Discrete(NUMBER_OF_CORPORATIONS),
        })

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.player1 = None
        self.player2 = None
        self.player3 = None

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
        result = self.create_game(json.dumps(settings))

        self.player1 = Player(result["players"][0]["color"],
                              result["players"][0]["id"],
                              result["players"][0]["name"])
        self.player2 = Player(result["players"][1]["color"],
                              result["players"][1]["id"],
                              result["players"][1]["name"])
        self.player3 = Player(result["players"][2]["color"],
                              result["players"][2]["id"],
                              result["players"][2]["name"])

        res_player1 = self.get_game(self.player1)
        res_player2 = self.get_game(self.player2)
        res_player3 = self.get_game(self.player3)

        self.run_id = res_player1["runId"]  # all players have the same run_id

        self.player_on_turn = self.get_current_player(res_player1["players"]) # the three res are not equal but show the same current player

        self.observed_player = random.choice([self.player1, self.player2, self.player3])

        # TODO current_player ist eig nicht richtig. es geht um die view, welcher spieler über das gesamte spiel betrachtet wird. das darf
        # TODO sich nicht pro zug/runde ändern

        observation_player1 = self.create_observation_from_res(res_player1)
        observation_player2 = self.create_observation_from_res(res_player2)
        observation_player3 = self.create_observation_from_res(res_player3)

        match self.observed_player:
            case self.player1:
                # calc player 2 and 3 now
                action_player2, _ = self.policy_model.predict(observation_player2, deterministic=False)
                _ = self.normal_turn(action_player2)
                action_player3, _ = self.policy_model.predict(observation_player3, deterministic=False)
                _ = self.normal_turn(action_player3)
                return observation_player1, {}
            case self.player2:
                # calc player 1 and 3 now
                action_player1, _ = self.policy_model.predict(observation_player1, deterministic=False)
                _ = self.normal_turn(action_player1)
                action_player3, _ = self.policy_model.predict(observation_player3, deterministic=False)
                _ = self.normal_turn(action_player3)
                return observation_player2, {}
            case self.player3:
                action_player1, _ = self.policy_model.predict(observation_player1, deterministic=False)
                _ = self.normal_turn(action_player1)
                action_player2, _ = self.policy_model.predict(observation_player2, deterministic=False)
                _ = self.normal_turn(action_player2)
                return observation_player3, {}

        # return {
        #     AVAILABLE_ACTION_OPTIONS: None,
        #     SELECTED_ACTION_INDEX: None,
        #     "available_corporations": self.available_corporations.sample(),
        #     "available_initial_project_cards": self.available_initial_project_cards.sample(),
        # }, {}

    def get_current_player(self, players) -> Player:
        for player in players:
            if player["isActive"]:
                match player["color"]:
                    case self.player1.color:
                        return self.player1
                    case self.player2.color:
                        return self.player2
                    case self.player3.color:
                        return self.player3

    def create_observation_from_res(self, res):
        pass

    def step(self, action):
        res = None

        res = self.normal_turn(action)
        obs = self.create_observation_from_res(res)

        current_phase = "initial_research" # calc from res

        if current_phase == "drafting":
            all_players = [self.player1, self.player2, self.player3]
            all_players.remove(self.observed_player)
            res1 = self.get_game(all_players[0])
            obs1 = self.create_observation_from_res(res1)
            act1, _ = self.policy_model.predict(obs1, deterministic=False)
            _ = self.normal_turn(act1)
            res2 = self.get_game(all_players[1])
            obs2 = self.create_observation_from_res(res2)
            act2, _ = self.policy_model.predict(obs2, deterministic=False)
            _ = self.normal_turn(act2)
            # return obs usw




            res_player1 = self.get_game(self.player1)
            res_player2 = self.get_game(self.player2)
            res_player3 = self.get_game(self.player3)
            observation_player1 = self.create_observation_from_res(res_player1)
            observation_player2 = self.create_observation_from_res(res_player2)
            observation_player3 = self.create_observation_from_res(res_player3)
            match self.observed_player:
                case self.player1:
                    # calc player 2 and 3 now
                    action_player2, _ = self.policy_model.predict(observation_player2, deterministic=False)
                    _ = self.normal_turn(action_player2)
                    action_player3, _ = self.policy_model.predict(observation_player3, deterministic=False)
                    _ = self.normal_turn(action_player3)
                    # return
                case self.player2:
                    pass
                case self.player3:
                    pass
        else:
            curr_p = self.get_current_player(res["players"])
            # play turns of other players
            while self.player_on_turn != self.observed_player:
                pass # do the turn of the other players (is not necessarily two

            game = self.get_game(curr_p.id)
            obs = self.create_observation_from_res(game)
            # return









        match (self.last_observation["current_phase"]):
            case PhasesEnum.DRAFTING.value:
                pass
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

        self.player_on_turn = self.player1 # je nach observation festlegen

        return observation, reward, done, False, {}

    def create_game(self, payload):
        self.http_connection.request("PUT", "/game", body=payload)
        response = self.http_connection.getresponse()
        result = json.loads(response.read().decode())
        return result

    def send_player_input(self, player_id, payload):
        self.http_connection.request("POST", "/player/input?id=" + player_id, body=payload)
        response = self.http_connection.getresponse()
        result = json.loads(response.read().decode())
        return result

    def get_game(self, player_id):
        self.http_connection.request("GET", "/api/player?id=" + player_id)
        response = self.http_connection.getresponse()
        return json.loads(response.read().decode())

    def normal_turn(self, action):

        # this action is to be used on self.player_on_turn

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

        run_id = self.player_on_turn.run_id


        if "options" in current_state["waitingFor"]:
            # this has to be handled separately bc the options are not really options but all mandatory
            if current_state["waitingFor"]["title"] == "Initial Research Phase":
                selected_corporation_name = ALL_CORPORATIONS_INDEX_NAME[action[SELECTED_CORPORATION]]
                available_cash_for_project_cards = CORPORATIONS_STARTING_MC[selected_corporation_name]

                available_cards = current_state["waitingFor"]["options"][2]["cards"]
                selected_cards_indices = action[MULTIPLE_SELECTED_CARDS]
                selected_project_cards = []
                for card_index, selected_binary in enumerate(selected_cards_indices):
                    if selected_binary == 1:
                        selected_card_name: str = CARD_NAMES_INT_STR[card_index]
                        for card in available_cards:
                            if card["name"] == selected_card_name:
                                selected_project_cards.append(card)
                                break


                while True:
                    cost_of_card_selection = sum(map(lambda card: card["calculatedCost"], selected_project_cards))
                    if cost_of_card_selection > available_cash_for_project_cards:
                        most_expensive_card_index = argmax(map(lambda card: card["calculatedCost"], selected_project_cards))
                        selected_project_cards.pop(most_expensive_card_index)
                    else:
                        break

                selected_project_card_names = list(map(lambda card: card["name"], selected_project_cards))

                selected_prelude_cards_indices = action[TWO_SELECTED_CARDS_INDICES]
                selected_prelude_cards_names = []
                for card_index, selected_binary in enumerate(selected_prelude_cards_indices):
                    if selected_binary == 1:
                        selected_card_name: str = CARD_NAMES_INT_STR[card_index]
                        selected_prelude_cards_names.append(selected_card_name)

                payload = self.create_initial_cards_card_card_card_response(run_id, selected_corporation_name, selected_prelude_cards_names, selected_project_card_names)
            else: # wenn optionen ganz normal tatsächlich optionen sind
                available_options = current_state["waitingFor"]["options"]

                # TODO if index = standard project, check if is available and maybe choose other

                # die available options müssen noch von den namen her auf die korrekten indizes gemapped werden
                selected_option_from_all: str = ACTION_OPTIONS_INDEX_NAME[action[SELECTED_ACTION_OPTION_INDEX]]
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
                          "Take first action of ${0} corporation", #c = which_option["title"]["data"][0]["value"]
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

                        reserve_units = selected_card["reserveUnits"] if "reserveUnits" in selected_card else None
                        reserve_heat = 0
                        reserve_mc = 0
                        reserve_titanium = 0
                        reserve_steel = 0
                        if reserve_units:
                            reserve_heat = reserve_units["heat"]
                            reserve_mc = reserve_units["megacredits"]
                            reserve_steel = reserve_units["steel"]
                            reserve_titanium = reserve_units["titanium"]

                        payment_options = selected_option["paymentOptions"]
                        can_pay_with_heat = payment_options["heat"]
                        can_pay_with_steel = card_name in BUILDING_CARDS_SET  # building cards
                        can_pay_with_titanium = card_name in SPACE_CARDS_SET  # space cards
                        can_pay_with_microbes = False
                        if card_name in PLANT_CARDS_SET:
                            for p in current_state["players"]:
                                if p["color"] == self.player_on_turn.color:
                                    for card in p["tableau"]:
                                        if card["name"] == "Psychrophiles":
                                            can_pay_with_microbes = True
                                            break
                                    break

                        pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes = self.calc_payment_for_project_card(action,
                                                                                                                     current_state,
                                                                                                                     card_cost,
                                                                                                                     can_pay_with_heat,
                                                                                                                     can_pay_with_steel,
                                                                                                                     can_pay_with_titanium,
                                                                                                                     can_pay_with_microbes,
                                                                                                                     reserve_heat,
                                                                                                                     reserve_mc,
                                                                                                                     reserve_titanium,
                                                                                                                     reserve_steel)

                        payload = self.create_or_resp_project_card_payment(run_id, selected_option_index, card_name, pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes)
                    case "Sell patents": # multiple cards
                        selected_project_cards = []
                        selected_card_indices = action[MULTIPLE_SELECTED_CARDS]
                        for idx, binary in enumerate(selected_card_indices):
                            if binary == 1:
                                selected_card_name: str = CARD_NAMES_INT_STR[idx]
                                selected_project_cards.append(selected_card_name)
                        payload = self.create_or_resp_card_cards(run_id, selected_option_index, selected_project_cards)
                    case "Perform an action from a played card":
                        available_cards = selected_option["cards"]
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_FROM_PLAYED_CARDS_INDEX]]
                        payload = self.create_or_resp_card_cards(run_id, selected_option_index, [selected_card_from_all_name])
                    case ("Select a card to discard", # single card
                          "Add 3 microbes to a card",
                          "Select card to add 2 microbes",
                          "Select card to remove 2 Animal(s)",
                          "Select card to add 2 animals",
                          "Select card to add 4 animals",
                          "Add 2 animals to a card"):
                        available_cards = selected_option["cards"]
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_INDEX]]
                        payload = self.create_or_resp_card_cards(run_id, selected_option_index, [selected_card_from_all_name])
                    case ("Select space for greenery tile",
                          "Convert ${0} plants into greenery"):
                        available_spaces_ids = selected_option["spaces"]
                        selected_space_index = action[SELECTED_SPACE_INDEX]
                        selected_space_id = str(selected_space_index + 1) # TODO maybe "1" is not treated the same as "01"
                        payload = self.create_or_resp_space_space_id(run_id, selected_option_index, selected_space_id)
                    case "Select adjacent player to remove 4 M€ from":
                        available_players_colors = selected_option["players"]
                        selected_player_index = action[SELECTED_PLAYER]
                        selected_player_color = PLAYERS_ID_COLOR[selected_player_index]
                        payload = self.create_or_resp_player_player(run_id, selected_option_index, selected_player_color)
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
                        # wenn das SP nicht verfügbar ist, darf es gar nicht erst als option im beobachtungsraum sein
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
                    available_spaces_ids = current_state["waitingFor"]["spaces"]
                    selected_space_index_from_all = action[SELECTED_SPACE_INDEX]
                    selected_space_id = str(selected_space_index_from_all + 1)
                    payload = self.create_space_id_response(run_id, selected_space_id)
                case "Select player to decrease ${0} production by ${1} step(s)":
                    selected_player_index = action[SELECTED_PLAYER]
                    selected_player_color = PLAYERS_ID_COLOR[selected_player_index]
                    payload = self.create_player_response(run_id, selected_player_color)
                case ("Select card to add ${0} ${1}", # geschenkt
                      "Select builder card to copy",
                      "Select 1 card(s) to keep",
                      "Select card to remove 1 Microbe(s)",
                      "Select card to remove 1 Animal(s)",
                      "Select prelude card to play",
                      "Select a card to keep and pass the rest to ${0}"):
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_INDEX]]
                    payload = self.create_cards_response(run_id, [selected_card_from_all_name])
                case "Select card(s) to buy":  # 0 or 1
                    available_cards = current_state["waitingFor"]["cards"]
                    max_amount_of_cards = current_state["waitingFor"]["max"]
                    if max_amount_of_cards == 1:
                        selected_cards_names = []
                        if action[DONT_BUY_CARD] == 1:
                            selected_card_index = action[SELECTED_CARD_INDEX]
                            selected_card_from_all_name: str = CARD_NAMES_INT_STR[selected_card_index]
                            selected_cards_names = [selected_card_from_all_name]
                        elif action[DONT_BUY_CARD] == 0:
                            pass
                        payload = self.create_cards_response(run_id, selected_cards_names)
                    elif max_amount_of_cards == 4:
                        selected_cards_names = []
                        selected_card_indices = action[MULTIPLE_SELECTED_RESEARCH_CARDS]
                        for idx, binary in enumerate(selected_card_indices):
                            if binary == 1:
                                selected_card_name: str = CARD_NAMES_INT_STR[idx]
                                selected_cards_names.append(selected_card_name)
                        payload = self.create_cards_response(run_id, selected_cards_names)
                case "Select 2 card(s) to keep":
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_cards_indices = action[TWO_SELECTED_CARDS_INDICES]
                    selected_cards_names = []
                    for idx, binary in enumerate(selected_cards_indices):
                        if binary == 1:
                            selected_card_name: str = CARD_NAMES_INT_STR[idx]
                            selected_cards_names.append(selected_card_name)

                    if len(selected_cards_names) != 2:
                        print("did not correctly select 2 cards")
                        exit(-458764)
                    self.create_cards_response(run_id, selected_cards_names)
                case "You cannot afford any cards":
                    self.create_cards_response(run_id, [])
                case "Play project card":
                    available_cards = current_state["waitingFor"]["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_INDEX]]
                    selected_card = None
                    for card in available_cards:
                        if card["name"] == selected_card_from_all_name:
                            selected_card = card
                            break

                    card_cost = selected_card["calculatedCost"]
                    card_name = selected_card["name"]

                    reserve_units = selected_card["reserveUnits"] if "reserveUnits" in selected_card else None
                    reserve_heat = 0
                    reserve_mc = 0
                    reserve_titanium = 0
                    reserve_steel = 0
                    if reserve_units:
                        reserve_heat = reserve_units["heat"]
                        reserve_mc = reserve_units["megacredits"]
                        reserve_steel = reserve_units["steel"]
                        reserve_titanium = reserve_units["titanium"]

                    payment_options = current_state["waitingFor"]["paymentOptions"]
                    can_pay_with_heat = payment_options["heat"]
                    can_pay_with_steel = card_name in BUILDING_CARDS_SET  # building cards
                    can_pay_with_titanium = card_name in SPACE_CARDS_SET  # space cards
                    can_pay_with_microbes = False
                    if card_name in PLANT_CARDS_SET:
                        for p in current_state["players"]:
                            if p["color"] == self.player_on_turn.color:
                                for card in p["tableau"]:
                                    if card["name"] == "Psychrophiles":
                                        can_pay_with_microbes = True
                                        break
                                break

                    pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes = self.calc_payment_for_project_card(action,
                                                                                                                 current_state,
                                                                                                                 card_cost,
                                                                                                                 can_pay_with_heat,
                                                                                                                 can_pay_with_steel,
                                                                                                                 can_pay_with_titanium,
                                                                                                                 can_pay_with_microbes,
                                                                                                                 reserve_heat,
                                                                                                                 reserve_mc,
                                                                                                                 reserve_titanium,
                                                                                                                 reserve_steel)

                    self.create_project_card_payment_response(run_id, card_name, pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes)
                    pass
                case ("Select how to pay for the ${0} standard project",
                      "Select how to spend ${0} M€",
                      "Select how to spend ${0} M€ for ${1} cards",
                      "Select how to pay for ${0} action", # too complicated
                      "Select how to pay for award",
                      "Select how to pay for action",
                      "Select how to pay for milestone"):

                    cost = current_state["waitingFor"]["amount"]

                    payment_options = current_state["waitingFor"]["paymentOptions"]
                    can_pay_with_heat = payment_options["heat"]
                    can_pay_with_titanium = payment_options["titanium"]
                    can_pay_with_steel = payment_options["steel"]

                    pay_heat, pay_mc, pay_steel, pay_titanium, _ = self.calc_payment_for_project_card(action,
                                                                                                     current_state,
                                                                                                     cost,
                                                                                                     can_pay_with_heat,
                                                                                                     can_pay_with_steel,
                                                                                                     can_pay_with_titanium,
                                                                                                     False,
                                                                                                     0,
                                                                                                     0,
                                                                                                     0,
                                                                                                     0)
                    payload = self.create_payment_response(run_id, pay_heat, pay_mc, pay_steel, pay_titanium)
                case "Select amount of heat production to decrease":
                    selected_amount = action[AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE]
                    #min = current_state["waitingFor"]["min"]
                    max = current_state["waitingFor"]["max"]
                    amount = min(selected_amount, max)
                    payload = self.create_amount_response(run_id, amount)
                case "Select amount of energy to spend":
                    selected_amount = action[AMOUNT_OF_ENERGY_TO_SPEND]
                    max = current_state["waitingFor"]["max"]
                    amount = min(selected_amount, max)
                    payload = self.create_amount_response(run_id, amount)

        res = self.send_player_input(self.player_on_turn.id, payload)
        # from this res create new observation

        # send_player_input(json.dumps(select_space_data), player.id, http_connection)
        return res

    def calc_payment_for_project_card(self,
                                      action,
                                      current_state,
                                      cost,
                                      can_pay_with_heat,
                                      can_pay_with_steel,
                                      can_pay_with_titanium,
                                      can_pay_with_microbes,
                                      reserve_heat,
                                      reserve_mc,
                                      reserve_titanium,
                                      reserve_steel):

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

        available_heat -= reserve_heat
        available_mc -= reserve_mc
        available_titanium -= reserve_titanium
        available_steel -= reserve_steel

        pay_heat = math.floor(pay_heat_percentage * available_heat) * (1 if can_pay_with_heat else 0)
        pay_mc = math.floor(pay_mc_percentage * available_mc)
        pay_steel = math.floor(pay_steel_percentage * available_steel) * (1 if can_pay_with_steel else 0)
        pay_titanium = math.floor(pay_titanium_percentage * available_titanium) * (1 if can_pay_with_titanium else 0)
        pay_microbes = math.floor(pay_microbes_percentage * available_microbes) * (1 if can_pay_with_microbes else 0)

        payment = pay_heat + pay_mc + pay_steel * steel_value + pay_titanium * titanium_value + pay_microbes * microbes_value

        if payment != cost:
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
                elif payment == "microbes":
                    if available_microbes * microbes_value >= remaining_cost:
                        pay_microbes = math.ceil(remaining_cost / microbes_value)
                        break
                    else:
                        pay_microbes = available_microbes
                        remaining_cost = remaining_cost - available_microbes * microbes_value

        return pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes

    def create_or_resp_option(self, run_id, index):
        return {
            "runId": run_id,
            "type": "or",
            "index": index,
            "response": {
                "type": "option"
            }
        }

    def create_initial_cards_card_card_card_response(self, run_id, corporation_card_name, prelude_cards_names, project_cards_names):
        return {
            "runId": run_id,
            "type": "initialCards",
            "responses": [
                {
                    "type": "card",
                    "cards": [corporation_card_name]
                }, {
                    "type": "card",
                    "cards": prelude_cards_names
                }, {
                    "type": "card",
                    "cards": project_cards_names
                }]
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
