from enum import Enum
from typing import Dict

BUILDING_CARDS_SET = {'Smelting Plant', 'SF Memorial', 'Self-Sufficient Settlement', 'Polar Industries',
                      'Mohole Excavation', 'Mohole', 'Mining Operations', 'Martian Industries', 'Lava Tube Settlement',
                      'House Printing', 'Early Settlement', 'Dome Farming', 'Cheung Shing MARS', 'AI Central',
                      'Aquifer Pumping', 'Artificial Lake', 'Biomass Combustors', 'Building Industries', 'Capital',
                      'Carbonate Processing', 'Colonizer Training Camp', 'Commercial District', 'Corporate Stronghold',
                      'Cupola City', 'Deep Well Heating', 'Development Center', 'Domed Crater', 'Electro Catapult',
                      'Eos Chasma National Park', 'Equatorial Magnetizer', 'Food Factory', 'Fueled Generators',
                      'Fuel Factory', 'Fusion Power', 'Geothermal Power', 'GHG Factories', 'Great Dam', 'Greenhouses',
                      'Heat Trappers', 'Immigrant City', 'Industrial Center', 'Industrial Microbes', 'Ironworks',
                      'Magnetic Field Dome', 'Magnetic Field Generators', 'Mars University', 'Martian Rails',
                      'Medical Lab', 'Mine', 'Mining Area', 'Mining Rights', 'Mining Rights', 'Mining Rights',
                      'Mohole Area', 'Natural Preserve', 'Noctis City', 'Noctis Farming', 'Nuclear Power',
                      'Olympus Conference', 'Open City', 'Ore Processor', 'Peroxide Power', 'Physics Complex',
                      'Power Infrastructure', 'Power Plant', 'Protected Valley', 'Rad-Chem Factory', 'Research Outpost',
                      'Rover Construction', 'Soil Factory', 'Solar Power', 'Space Elevator', 'Steelworks', 'Strip Mine',
                      'Tectonic Stress Power', 'Titanium Mine', 'Tropical Resort', 'Underground City',
                      'Underground Detonations', 'Urbanized Area', 'Water Splitting Plant', 'Windmills'}

SPACE_CARDS_SET = {'Space Hotels', 'Point Luna', 'Orbital Construction Yard', 'Space Elevator',
                   'Aerobraked Ammonia Asteroid', 'Asteroid', 'Asteroid Mining', 'Beam From A Thorium Asteroid',
                   'Big Asteroid', 'Callisto Penal Mines', 'Comet', 'Convoy From Europa', 'Deimos Down',
                   'Ganymede Colony', 'Giant Ice Asteroid', 'Giant Space Mirror', 'Ice Asteroid',
                   'Immigration Shuttles', 'Imported GHG', 'Imported Hydrogen', 'Imported Nitrogen',
                   'Import of Advanced GHG', 'Interstellar Colony Ship', 'Io Mining Industries', 'Lagrange Observatory',
                   'Large Convoy', 'Methane From Titan', 'Miranda Resort', 'Nitrogen-Rich Asteroid',
                   'Optimal Aerobraking', 'Phobos Space Haven', 'Satellites', 'Security Fleet', 'Shuttles',
                   'Solar Wind Power', 'Soletta', 'Space Mirrors', 'Space Station', 'Technology Demonstration',
                   'Terraforming Ganymede', 'Toll Station', 'Towing A Comet', 'Trans-Neptune Probe', 'Vesta Shipyard',
                   'Water Import From Europa'}

PLANT_CARDS_SET = {'Biosphere Support', 'Dome Farming', 'Ecology Experts', 'Experimental Forest', 'Adapted Lichen',
                   'Advanced Ecosystems', 'Algae', 'Arctic Algae', 'Bushes', 'Ecological Zone',
                   'Eos Chasma National Park', 'Farming', 'Grass', 'Greenhouses', 'Heather', 'Kelp Farming', 'Lichen',
                   'Mangrove', 'Moss', 'Nitrophilic Moss', 'Noctis Farming', 'Plantation', 'Protected Valley', 'Trees',
                   'Tundra Farming'}

NUMBER_PLAYERS = 3
NUMBER_PLAYERS_DISCRETE = 4

NONE_PLAYER_INDEX = 3

NUMBER_SPACES = 63  # indices 01 to 63




class PhasesEnum(Enum):
    INITIAL_RESEARCH = 0,
    RESEARCH = 1,
    ACTION = 2,
    PRODUCTION = 3,
    DRAFTING = 4,
    END = 5,
    PRELUDES = 6,


PHASES_STR_INT: Dict[str, int] = {
    "research": 0,
    "preludes": 1,
    "action": 2,
    "production": 3,
    "drafting": 4,
    "end": 5,
}

AWARDS_INT_STR: Dict[int, str] = {
    0: "Miner",
    1: "Scientist",
    2: "Landlord",
    3: "Thermalist",
    4: "Banker",
}

AWARDS_STR_INT = {
    "Miner": 0,
    "Scientist": 1,
    "Landlord": 2,
    "Thermalist": 3,
    "Banker": 4,
}

def NUMBER_OF_AWARDS(): return len(AWARDS_INT_STR)
NUMBER_OF_AWARDS_DISCRETE = NUMBER_OF_AWARDS() + 1
NONE_AWARD_INDEX = 5

MILESTONES_INT_STR: Dict[int, str] = {
    0: "Gardener",
    1: "Mayor",
    2: "Terraformer",
    3: "Planner",
    4: "Builder",
}

MILESTONES_STR_INT: Dict[str, int] = {
    "Gardener": 0,
    "Mayor": 1,
    "Terraformer": 2,
    "Planner": 3,
    "Builder": 4,
}

STANDARD_PROJECTS_INDEX_NAME: Dict[int, str] = {
    0: "Power Plant:SP",
    1: "Asteroid:SP",
    2: "Aquifer",
    3: "Greenery",
    4: "City"
}

STANDARD_PROJECTS_NAME_INDEX = {
    "Power Plant:SP": 0,
    "Asteroid:SP": 1,
    "Aquifer": 2,
    "Greenery": 3,
    "City": 4,
}

def NUMBER_OF_MILESTONES(): return len(MILESTONES_INT_STR)


def NUMBER_OF_STANDARD_PROJECTS(): return len(STANDARD_PROJECTS_INDEX_NAME)
NUMBER_OF_STANDARD_PROJECTS_DISCRETE = NUMBER_OF_STANDARD_PROJECTS() + 1
NONE_STANDARD_PROJECT_INDEX = 5


def get_index_of_player_color_by_current_player_color(color_of_player, color_of_current_player):
    color_order = {
        "red": ["yellow", "red", "green"],
        "green": ["red", "green", "yellow"],
        "yellow": ["green", "yellow", "red"]
    }
    return color_order[color_of_current_player].index(color_of_player)


def get_color_of_player_index_by_current_player_color(index_of_player, color_of_current_player):
    color_order = {
        "red": ["yellow", "red", "green"],
        "green": ["red", "green", "yellow"],
        "yellow": ["green", "yellow", "red"]
    }
    return color_order[color_of_current_player][index_of_player]


SELECTED_ACTION_OPTION_NAME_INDEX: Dict[str, int] = {
    "Select space for ${0} tile": 0,
    "Select space for ocean tile": 1,
    "Select space reserved for ocean to place greenery tile": 3,
    "Select a space with a steel or titanium bonus": 4,
    "Select space adjacent to a city tile": 5,
    "Select place next to no other tile for city": 6,
    "Select space next to greenery for special tile": 7,
    "Select either Tharsis Tholus, Ascraeus Mons, Pavonis Mons or Arsia Mons": 8,
    "Select a space with a steel or titanium bonus adjacent to one of your tiles": 9,
    "Select space next to at least 2 other city tiles": 10,
    "Select a land space to place an ocean tile": 11,
    "Select space for city tile": 12,
    "Select space for greenery tile": 13,
    "Select space for ocean from temperature increase": 14,
    "Select space for claim": 15,
    "Select space for first ocean": 16,
    "Select space for second ocean": 17,
    "Select space for special city tile": 18,
    "Select player to decrease ${0} production by ${1} step(s)": 19,
    "Select card to add ${0} ${1}": 20,
    "Select builder card to copy": 21,
    "Select 1 card(s) to keep": 22,
    "Select card to remove 1 Microbe(s)": 23,
    "Select card to remove 1 Animal(s)": 24,
    "Select prelude card to play": 25,
    "Select a card to keep and pass the rest to ${0}": 26,
    "Select card(s) to buy": 27,
    "Select 2 card(s) to keep": 28,
    "You cannot afford any cards": 29,
    "Play project card": 30,
    "Select how to pay for the ${0} standard project": 31,
    "Select how to spend ${0} M€": 32,
    "Select how to spend ${0} M€ for ${1} cards": 33,
    "Select how to pay for ${0} action": 34,
    "Select how to pay for award": 35,
    "Select how to pay for action": 36,
    "Select how to pay for milestone": 37,
    "Select amount of heat production to decrease": 38,
    "Select amount of energy to spend": 2,
    "Initial Research Phase": 39,
    "None": 40,
}
NUMBER_ALL_ACTIONS = len(SELECTED_ACTION_OPTION_NAME_INDEX)  # without action options

ACTION_OPTIONS_NAME_INDEX: Dict[str, int] = {
    "Pass for this generation": 0,
    "End turn": 1,
    "Convert 8 heat into temperature": 2,
    "Convert 8 plants into greenery": 3,
    "Do nothing": 4,
    "Skip removal": 5,
    "Skip removing plants": 6,
    "Increase your plant production 1 step": 7,
    "Add a science resource to this card": 8,
    "Do not remove resource": 9,
    "Increase your energy production 2 steps": 10,
    "Increase titanium production 1 step": 11,
    "Increase megacredits production 1 step": 12,
    "Increase steel production 1 step": 13,
    "Increase plants production 1 step": 14,
    "Increase heat production 1 step": 15,
    "Increase energy production 1 step": 16,
    "Do not steal": 17,
    "Remove 2 microbes to raise oxygen level 1 step": 18,
    "Add 1 microbe to this card": 19,
    "Remove 3 microbes to increase your terraform rating 1 step": 20,
    "Don't place a greenery": 21,
    "Remove a science resource from this card to draw a card": 22,
    "Spend 1 steel to gain 7 M€.": 23,
    "Remove 2 microbes to raise temperature 1 step": 24,
    "Gain 4 plants": 25,
    "Spend 1 plant to gain 7 M€.": 26,
    "Gain plant": 27,
    "Gain 1 plant": 28,
    "Gain 3 plants": 29,
    "Gain 5 plants": 30,
    "Don't remove M€ from adjacent player": 31,
    "Take first action of ${0} corporation": 32,
    "Remove ${0} plants from ${1}": 33,
    "Remove ${0} ${1} from ${2}": 34,
    "Steal ${0} M€ from ${1}": 35,
    "Steal ${0} steel from ${1}": 36,
    "Add ${0} microbes to ${1}": 37,
    "Add resource to card ${0}": 38,
    "Add ${0} animals to ${1}": 39,
    "Fund ${0} award": 40,
    "Play project card": 41,
    "Sell patents": 42,
    "Perform an action from a played card": 43,
    "Select a card to discard": 44,
    "Add 3 microbes to a card": 45,
    "Select card to add 2 microbes": 46,
    "Select card to remove 2 Animal(s)": 47,
    "Select card to add 2 animals": 48,
    "Select card to add 4 animals": 49,
    "Add 2 animals to a card": 50,
    "Select space for greenery tile": 51,
    "Convert ${0} plants into greenery": 52,
    "Select adjacent player to remove 4 M€ from": 53,
    "Fund an award (${0} M€)": 54,
    "Standard projects": 55,
    "Claim a milestone": 56,
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

NUMBER_ALL_ACTION_OPTIONS = len(ACTION_OPTIONS_INDEX_NAME)

CARD_NAMES_STR_INT: Dict[str, int] = {
    "Sell Patents": 0,
    "Power Plant:SP": 1,
    "Asteroid:SP": 2,
    "Buffer Gas": 3,
    "Aquifer": 4,
    "Greenery": 5,
    "City": 6,
    "Convert Plants": 7,
    "Convert Heat": 8,
    "Acquired Company": 9,
    "Adaptation Technology": 10,
    "Adapted Lichen": 11,
    "Advanced Alloys": 12,
    "Advanced Ecosystems": 13,
    "Aerobraked Ammonia Asteroid": 14,
    "AI Central": 15,
    "Air Raid": 16,
    "Algae": 17,
    "Anti-Gravity Technology": 18,
    "Ants": 19,
    "Aquifer Pumping": 20,
    "Aquifer Turbines": 21,
    "ArchaeBacteria": 22,
    "Artificial Lake": 23,
    "Artificial Photosynthesis": 24,
    "Arctic Algae": 25,
    "Asteroid": 26,
    "Asteroid Mining": 27,
    "Asteroid Mining Consortium": 28,
    "Breathing Filters": 29,
    "Bribed Committee": 30,
    "Beam From A Thorium Asteroid": 31,
    "Big Asteroid": 32,
    "Biomass Combustors": 33,
    "Birds": 34,
    "Black Polar Dust": 35,
    "Building Industries": 36,
    "Bushes": 37,
    "Business Contacts": 38,
    "Business Network": 39,
    "Callisto Penal Mines": 40,
    "Carbonate Processing": 41,
    "Capital": 42,
    "Caretaker Contract": 43,
    "Cartel": 44,
    "CEO's Favorite Project": 45,
    "Cloud Seeding": 46,
    "Colonizer Training Camp": 47,
    "Comet": 48,
    "Commercial District": 49,
    "Convoy From Europa": 50,
    "Corporate Stronghold": 51,
    "Cupola City": 52,
    "Decomposers": 53,
    "Deep Well Heating": 54,
    "Deimos Down": 55,
    "Designed Microorganisms": 56,
    "Development Center": 57,
    "Dirigibles": 58,
    "Dome Farming": 59,
    "Domed Crater": 60,
    "Dust Seals": 61,
    "Early Settlement": 62,
    "Earth Catapult": 63,
    "Earth Office": 64,
    "Eccentric Sponsor": 65,
    "Ecological Zone": 66,
    "Ecology Experts": 67,
    "Electro Catapult": 68,
    "Energy Saving": 69,
    "Energy Tapping": 70,
    "Eos Chasma National Park": 71,
    "Equatorial Magnetizer": 72,
    "Extreme-Cold Fungus": 73,
    "Farming": 74,
    "Fish": 75,
    "Flooding": 76,
    "Food Factory": 77,
    "Fuel Factory": 78,
    "Fueled Generators": 79,
    "Fusion Power": 80,
    "Ganymede Colony": 81,
    "Gene Repair": 82,
    "Geothermal Power": 83,
    "GHG Producing Bacteria": 84,
    "GHG Factories": 85,
    "Giant Ice Asteroid": 86,
    "Giant Space Mirror": 87,
    "Grass": 88,
    "Great Aquifer": 89,
    "Great Dam": 90,
    "Great Escarpment Consortium": 91,
    "Greenhouses": 92,
    "Gyropolis": 93,
    "Hackers": 94,
    "Heather": 95,
    "Heat Trappers": 96,
    "Herbivores": 97,
    "Hired Raiders": 98,
    "House Printing": 99,
    "Ice Asteroid": 100,
    "Ice Cap Melting": 101,
    "Immigrant City": 102,
    "Immigration Shuttles": 103,
    "Imported GHG": 104,
    "Imported Hydrogen": 105,
    "Imported Nitrogen": 106,
    "Import of Advanced GHG": 107,
    "Indentured Workers": 108,
    "Industrial Microbes": 109,
    "Insects": 110,
    "Insulation": 111,
    "Interstellar Colony Ship": 112,
    "Invention Contest": 113,
    "Inventors' Guild": 114,
    "Investment Loan": 115,
    "Io Mining Industries": 116,
    "Ironworks": 117,
    "Kelp Farming": 118,
    "Lagrange Observatory": 119,
    "Lake Marineris": 120,
    "Land Claim": 121,
    "Large Convoy": 122,
    "Lava Flows": 123,
    "Lava Tube Settlement": 124,
    "Lichen": 125,
    "Lightning Harvest": 126,
    "Livestock": 127,
    "Local Heat Trapping": 128,
    "Lunar Beam": 129,
    "Magnetic Field Dome": 130,
    "Magnetic Field Generators": 131,
    "Martian Industries": 132,
    "Mangrove": 133,
    "Mars University": 134,
    "Martian Rails": 135,
    "Mass Converter": 136,
    "Media Archives": 137,
    "Media Group": 138,
    "Medical Lab": 139,
    "Methane From Titan": 140,
    "Micro-Mills": 141,
    "Mine": 142,
    "Mineral Deposit": 143,
    "Miranda Resort": 144,
    "Mining Area": 145,
    "Mining Expedition": 146,
    "Mining Operations": 147,
    "Mining Quota": 148,
    "Mining Rights": 149,
    "Mohole": 150,
    "Mohole Area": 151,
    "Mohole Excavation": 152,
    "Moss": 153,
    "Natural Preserve": 154,
    "Nitrite Reducing Bacteria": 155,
    "Nitrogen-Rich Asteroid": 156,
    "Nitrophilic Moss": 157,
    "Noctis City": 158,
    "Noctis Farming": 159,
    "Nuclear Power": 160,
    "Nuclear Zone": 161,
    "Olympus Conference": 162,
    "Omnicourt": 163,
    "Open City": 164,
    "Optimal Aerobraking": 165,
    "Ore Processor": 166,
    "Permafrost Extraction": 167,
    "Peroxide Power": 168,
    "Pets": 169,
    "Phobos Space Haven": 170,
    "Physics Complex": 171,
    "Plantation": 172,
    "Polar Industries": 173,
    "Power Grid": 174,
    "Power Infrastructure": 175,
    "Power Plant": 176,
    "Power Supply Consortium": 177,
    "Predators": 178,
    "Protected Habitats": 179,
    "Protected Valley": 180,
    "Psychrophiles": 181,
    "Quantum Extractor": 182,
    "Rad-Chem Factory": 183,
    "Rad-Suits": 184,
    "Regolith Eaters": 185,
    "Release of Inert Gases": 186,
    "Research": 187,
    "Research Outpost": 188,
    "Restricted Area": 189,
    "Robotic Workforce": 190,
    "Rover Construction": 191,
    "Sabotage": 192,
    "Satellites": 193,
    "Search For Life": 194,
    "Security Fleet": 195,
    "Self-Sufficient Settlement": 196,
    "Sister Planet Support": 197,
    "Small Animals": 198,
    "Soil Factory": 199,
    "Solar Power": 200,
    "Solarnet": 201,
    "Space Elevator": 202,
    "Strip Mine": 203,
    "Subterranean Reservoir": 204,
    "Shuttles": 205,
    "Solar Wind Power": 206,
    "Soletta": 207,
    "Space Mirrors": 208,
    "Space Station": 209,
    "Special Design": 210,
    "Sponsors": 211,
    "Steelworks": 212,
    "Standard Technology": 213,
    "Symbiotic Fungus": 214,
    "Tardigrades": 215,
    "Technology Demonstration": 216,
    "Tectonic Stress Power": 217,
    "Terraforming Ganymede": 218,
    "Titanium Mine": 219,
    "Toll Station": 220,
    "Towing A Comet": 221,
    "Trans-Neptune Probe": 222,
    "Trees": 223,
    "Tropical Resort": 224,
    "Tundra Farming": 225,
    "Underground City": 226,
    "Underground Detonations": 227,
    "Urbanized Area": 228,
    "Vesta Shipyard": 229,
    "Viral Enhancers": 230,
    "Virus": 231,
    "Water Import From Europa": 232,
    "Water Splitting Plant": 233,
    "Wave Power": 234,
    "Windmills": 235,
    "Worms": 236,
    "Zeppelins": 237,
    "Beginner Corporation": 238,
    "CrediCor": 239,
    "EcoLine": 240,
    "Helion": 241,
    "Interplanetary Cinematics": 242,
    "Inventrix": 243,
    "Mining Guild": 244,
    "PhoboLog": 245,
    "Saturn Systems": 246,
    "Teractor": 247,
    "Tharsis Republic": 248,
    "Thorgate": 249,
    "United Nations Mars Initiative": 250,
    "Acquired Space Agency": 251,
    "Allied Bank": 252,
    "Biofuels": 253,
    "Biolab": 254,
    "Biosphere Support": 255,
    "Business Empire": 256,
    "Cheung Shing MARS": 257,
    "Donation": 258,
    "Experimental Forest": 259,
    "Galilean Mining": 260,
    "Huge Asteroid": 261,
    "Io Research Outpost": 262,
    "Loan": 263,
    "Martian Survey": 264,
    "Metal-Rich Asteroid": 265,
    "Metals Company": 266,
    "Nitrogen Shipment": 267,
    "Orbital Construction Yard": 268,
    "Point Luna": 269,
    "Power Generation": 270,
    "Research Coordination": 271,
    "Research Network": 272,
    "Robinson Industries": 273,
    "SF Memorial": 274,
    "Smelting Plant": 275,
    "Society Support": 276,
    "Space Hotels": 277,
    "Supplier": 278,
    "Supply Drop": 279,
    "UNMI Contractor": 280,
    "Valley Trust": 281,
    "Vitor": 282,
    "Arcadian Communities": 283,
    "Astrodrill": 284,
    "Advertising": 285,
    "Pharmacy Union": 286,
    "Industrial Center": 287,
    "Factorum": 288,
    "Lakefront Resorts": 289,
    "Mons Insurance": 290,
    "Splice": 291,
    "Philares": 292,
    "Recyclon": 293,
    "Manutech": 294,
    "Self-replicating Robots": 295,
    "Polyphemos": 296,
    "Penguins": 297,
    "Small Asteroid": 298,
    "Snow Algae": 299
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
    22: "ArchaeBacteria",  # TODO maybe a bug
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

# NUMBER_OF_CARDS = 211 + 2 + 6 + 50 + 14 # 283
NUMBER_OF_CARDS = len(CARD_NAMES_INT_STR)

TILE_NAMES_OF_SELECTABLE_SPACES: Dict[str, int] = {
    "Mohole Area": 0,
    "Nuclear Zone": 1,
    "Commercial District": 2,
    "Restricted Area": 3,
    "Natural Preserve": 4,
    "None": 5
}

CORPORATIONS_WITH_FIRST_ACTION: Dict[str, int] = {
    "Valley Trust": 0,
    "Inventrix": 1,
    "Vitor": 2,
    "Tharsis Republic": 3,
    "None": 4,
}

REMOVABLE_RESOURCES_NAMES = {
    "M€": 0,
    "steel": 1,
    "titanium": 2,
    "None": 3
}

DECREASABLE_PRODUCTIONS_NAMES = {
    "megacredits": 0,
    "steel": 1,
    "titanium": 2,
    "heat": 3,
    "plants": 4,
    "energy": 5,
    "None": 6
}

CARDS_MICROBES_CAN_BE_ADDED_TO = {
    "Psychrophiles": 0,
    "GHG Producing Bacteria": 1,
    "Nitrite Reducing Bacteria": 2,
    "Tardigrades": 3,
    "Ants": 4,
    "Decomposers": 5,
    "None": 6
}

CARDS_RESOURCES_CAN_BE_ADDED_TO = {
    "Regolith Eaters": 0,
    "Tardigrades": 1,
    "GHG Producing Bacteria": 2,
    "Ecological Zone": 3,
    "Pets": 4,
    "Decomposers": 5,
}  # unused

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

ALL_CORPORATIONS_NAME_INDEX = {
    "CrediCor": 0,
    "EcoLine": 1,
    "Helion": 2,
    "Interplanetary Cinematics": 3,
    "Inventrix": 4,
    "Mining Guild": 5,
    "PhoboLog": 6,
    "Tharsis Republic": 7,
    "Thorgate": 8,
    "United Nations Mars Initiative": 9,
    "Saturn Systems": 10,
    "Teractor": 11,
    "Cheung Shing MARS": 12,
    "Point Luna": 13,
    "Robinson Industries": 14,
    "Valley Trust": 15,
    "Vitor": 16
}

NONE_CORPORATION_INDEX = 17

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
NUMBER_CORPORATIONS_DISCRETE = NUMBER_OF_CORPORATIONS + 1