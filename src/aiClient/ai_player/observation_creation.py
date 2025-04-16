import json

import numpy as np

from mapping_and_constants import *
from action_observation_names import *


def build_box_i8(value):
    return np.array([value], dtype=np.int8)


def build_discrete_i8(value):
    return np.int8(value)


# uses int16
def get_result_array_from_available_cards(available_cards):
    result = np.zeros(NUMBER_OF_CARDS, dtype=np.int16)
    if len(available_cards) == 0:
        result[CARD_NAMES_STR_INT["None"]] = 1
    else:
        for card in available_cards:
            card_name = card["name"]
            card_index = CARD_NAMES_STR_INT[card_name]
            result[card_index] = 1
    return result


def get_available_project_cards(res):
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    cards = {}
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Play project card":
                cards = option["cards"]
                break
    else:
        message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"]["title"] else \
        res["waitingFor"]["title"]
        if message == "Play project card":
            cards = res["waitingFor"]["cards"]
    return get_result_array_from_available_cards(cards)


def get_available_cards(res):
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    cards = {}
    if not is_action_option:
        message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"]["title"] else \
        res["waitingFor"]["title"]
        match message:
            case ("Select card to add ${0} ${1}",  # geschenkt
                  "Select builder card to copy",
                  "Select 1 card(s) to keep",
                  "Select card to remove 1 Microbe(s)",
                  "Select card to remove 1 Animal(s)",
                  "Select prelude card to play",
                  "Select a card to keep and pass the rest to ${0}",
                  "Select card(s) to buy"):
                cards = res["waitingFor"]["cards"]
    return get_result_array_from_available_cards(cards)


def get_available_cards_from_option(res, option_message):
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    cards = {}
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == option_message:
                cards = option["cards"]
                break
    return get_result_array_from_available_cards(cards)


def get_available_cards_to_discard(res):
    return get_available_cards_from_option(res, "Select a card to discard")


def get_available_cards_to_add_3_microbes_to(res):
    return get_available_cards_from_option(res, "Add 3 microbes to a card")


def get_available_cards_to_add_2_microbes_to(res):
    return get_available_cards_from_option(res, "Select card to add 2 microbes")


def get_available_cards_to_remove_2_animals_from(res):
    return get_available_cards_from_option(res, "Select card to remove 2 Animal(s)")


def get_available_cards_to_add_2_animals_to(res):
    return get_available_cards_from_option(res, "Select card to add 2 animals")


def get_available_cards_to_add_4_animals_to(res):
    return get_available_cards_from_option(res, "Select card to add 4 animals")


def get_available_cards_to_add_2_animals_to_2(res):
    return get_available_cards_from_option(res, "Add 2 animals to a card")


def get_available_spaces(res):
    result = np.zeros(NUMBER_SPACES, dtype=np.int8)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    available_spaces_ids = {}
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Select space for greenery tile" or message == "Convert ${0} plants into greenery":
                # theoretisch könnten beide optionen gleichzeitig verfügbar sein was es womöglich crashen würde
                # aber ich konnte nie beobachten dass das vorkam
                available_spaces_ids = option["spaces"]
                break
    else:
        message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"]["title"] else \
        res["waitingFor"]["title"]
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
                available_spaces_ids = res["waitingFor"]["spaces"]
    for space_id in available_spaces_ids:
        space_index = int(space_id) - 1
        result[space_index] = 1
    if sum(result) == 0:
        result[NONE_SPACE_INDEX] = 1
    return result


def get_available_players(res):
    result = np.zeros(NUMBER_PLAYERS, dtype=np.int8)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    available_player_colors = {}
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Select adjacent player to remove 4 M€ from":
                available_player_colors = option["players"]
    else:
        message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"]["title"] else \
            res["waitingFor"]["title"]
        if message == "Select player to decrease ${0} production by ${1} step(s)":
            available_player_colors = res["waitingFor"]["players"]
    color_of_this_player = res["thisPlayer"]["color"]
    for player_color in available_player_colors:
        index = get_index_of_player_color_by_current_player_color(player_color, color_of_this_player)
        result[index] = 1
    if sum(result) == 0:
        result[NONE_PLAYER_INDEX] = 1
    return result


def get_available_cards_with_actions(res):
    result = np.zeros(NUMBER_OF_CARDS, dtype=np.int16)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Perform an action from a played card":
                available_cards = option["cards"]
                for card in available_cards:
                    index_of_card = CARD_NAMES_STR_INT[card["name"]]
                    result[index_of_card] = 1
                break
    if sum(result) == 0:
        result[CARD_NAMES_STR_INT["None"]] = 1
    return result


def get_available_milestones(res):
    result = np.zeros(NUMBER_OF_MILESTONES(), dtype=np.int8)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Claim a milestone":
                available_milestones = option["options"]
                for milestone in available_milestones:
                    index_of_milestone = MILESTONES_STR_INT[milestone["title"]]
                    result[index_of_milestone] = 1
                break
    return result


def get_available_awards(res):
    result = np.zeros(NUMBER_OF_AWARDS(), dtype=np.int8)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Fund an award (${0} M€)":
                available_awards = option["options"]
                for award in available_awards:
                    index_of_award = AWARDS_STR_INT[award["title"]]
                    result[index_of_award] = 1
                break
    return result


def get_corporation_to_take_first_action_of(res):
    corporation_index = CORPORATIONS_WITH_FIRST_ACTION["None"]
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Take first action of ${0} corporation":
                corporation_name = option["title"]["data"][0]["value"]
                corporation_index = CORPORATIONS_WITH_FIRST_ACTION[corporation_name]
                break
    result = build_discrete_i8(corporation_index)
    return result


def get_available_standard_projects(res):
    result = np.zeros(NUMBER_OF_STANDARD_PROJECTS, dtype=np.int8)
    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"
    if is_action_option:
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            if message == "Standard projects":
                available_standard_projects = option["options"]
                for standard_project in available_standard_projects:
                    if "isDisabled" not in standard_project or (
                            "isDisabled" in standard_project and standard_project["isDisabled"] == "False"):
                        index_of_standard_project = STANDARD_PROJECTS_NAME_INDEX[standard_project["name"]]
                        result[index_of_standard_project] = 1
                break
    if sum(result) == 0:
        result[STANDARD_PROJECTS_NAME_INDEX["None"]] = 1
    return result


def get_resource_to_remove(action_option):
    resource_index = REMOVABLE_RESOURCES_NAMES["None"]
    if action_option:
        resource_name = action_option["title"]["data"][0]["value"]
        resource_index = REMOVABLE_RESOURCES_NAMES[resource_name]
    result = build_discrete_i8(resource_index)
    return result


def get_amount_from_action_option(action_option, index):
    amount = 0
    if action_option:
        amount = action_option["title"]["data"][index]["value"]
    result = build_box_i8(amount)
    return result


def get_player_from_action_option(res, action_option, index):
    player_index = NONE_PLAYER_INDEX
    if action_option:
        player_color = action_option["title"]["data"][index]["value"]
        color_of_this_player = res["thisPlayer"]["color"]
        player_index = get_index_of_player_color_by_current_player_color(player_color, color_of_this_player)
    result = build_discrete_i8(player_index)
    return result


def get_card_to_add_microbe_to(action_option, index):
    card_name = "None"
    if action_option:
        card_name = action_option["title"]["data"][index]["value"]
    card_index = CARDS_MICROBES_CAN_BE_ADDED_TO[card_name]
    return build_discrete_i8(card_index)


def get_award_to_fund(action_option, index):
    award_index = NONE_AWARD_INDEX
    if action_option:
        award_name = action_option["title"]["data"][index]["value"]
        award_index = AWARDS_STR_INT[award_name]
    return build_discrete_i8(award_index)


def get_fund_award_cost(action_option, index):
    cost = 0
    if action_option:
        cost = action_option["title"]["data"][index]["value"]
    cost_index = 0
    match cost:
        case 8:
            cost_index = 1
        case 14:
            cost_index = 2
        case 20:
            cost_index = 3
    return build_discrete_i8(cost_index)


def get_tile_to_select_space_for(action_option, index):
    tile_name = "None"
    if action_option:
        tile_name = action_option["title"]["data"][index]["value"]
    tile_index = TILE_NAMES_OF_SELECTABLE_SPACES[tile_name]
    return build_discrete_i8(tile_index)


def get_production_to_decrease(action_option, index):
    production_name = "None"
    if action_option:
        production_name = action_option["title"]["data"][index]["value"]
    production_index = DECREASABLE_PRODUCTIONS_NAMES[production_name]
    return build_discrete_i8(production_index)


def get_standard_project_to_select_how_to_pay_for(action_option, index):
    standard_project_index = STANDARD_PROJECTS_NAME_INDEX["None"]
    if action_option:
        standard_project_name = action_option["title"]["data"][index]["value"]
        standard_project_index = STANDARD_PROJECTS_NAME_INDEX[standard_project_name]
    return build_discrete_i8(standard_project_index)


def get_max_value(action_option):
    max_prod = 0
    if action_option:
        max_prod = action_option["max"]
    return build_box_i8(max_prod)


def get_available_corporations(res):
    available_corporations = np.zeros(NUMBER_OF_CORPORATIONS, dtype=np.int8)
    if "options" in res["waitingFor"] and res["waitingFor"]["title"] == "Initial Research Phase":
        for corporation in res["waitingFor"]["options"][0]["cards"]:
            corporation_name = corporation["name"]
            corporation_index = ALL_CORPORATIONS_NAME_INDEX[corporation_name]
            available_corporations[corporation_index] = 1
    return available_corporations


def get_picked_corporation(res):
    picked_corporation = NONE_CORPORATION_INDEX
    if "pickedCorporationCard" in res and len(res["pickedCorporationCard"]) > 0:
        picked_corporation = ALL_CORPORATIONS_NAME_INDEX[res["pickedCorporationCard"]["name"]]
    return build_discrete_i8(picked_corporation)


def get_cards_in_hand(res):
    cards_in_hand = np.zeros(len(CARD_NAMES_INT_STR), dtype=np.int16)
    for card in res["preludeCardsInHand"]:
        card_name = card["name"]
        card_index = CARD_NAMES_STR_INT[card_name]
        cards_in_hand[card_index] = 1
    for card in res["cardsInHand"]:
        card_name = card["name"]
        card_index = CARD_NAMES_STR_INT[card_name]
        cards_in_hand[card_index] = 1
    if len(res["preludeCardsInHand"]) == 0 and len(res["cardsInHand"]) == 0:
        cards_in_hand[CARD_NAMES_STR_INT["None"]] = 1
    return cards_in_hand


def get_dealt_cards(res):
    dealt_cards = np.zeros(len(CARD_NAMES_INT_STR), dtype=np.int16)
    for card in res["dealtPreludeCards"]:
        card_name = card["name"]
        card_index = CARD_NAMES_STR_INT[card_name]
        dealt_cards[card_index] = 1
    for card in res["dealtProjectCards"]:
        card_name = card["name"]
        card_index = CARD_NAMES_STR_INT[card_name]
        dealt_cards[card_index] = 1
    if len(res["dealtPreludeCards"]) == 0 and len(res["dealtProjectCards"]) == 0:
        dealt_cards[CARD_NAMES_STR_INT["None"]] = 1
    return dealt_cards


def get_current_phase(res):
    phase_name = res["game"]["phase"]
    phase_index = PHASES_STR_INT[phase_name]
    return build_discrete_i8(phase_index)


def get_occupied_spaces(res):
    occupied_spaces = np.full(NUMBER_SPACES, NONE_PLAYER_INDEX, dtype=np.int8)
    # occupied_spaces = np.zeros((NUMBER_SPACES,), dtype=np.int8)
    current_player_color = res["thisPlayer"]["color"]
    for space in res["game"]["spaces"]:
        if space["id"] == "69":
            continue  # aus ner erweiterung
        if "color" in space:
            player_color = space["color"]
            player_id = get_index_of_player_color_by_current_player_color(player_color, current_player_color)
            space_id = int(space["id"])
            occupied_spaces[space_id] = player_id
    return occupied_spaces


def create_observation_from_res(res):
    # res = {
    #     "waitingFor": {
    #         "title1": {
    #             "message": "Select space for ${0} tile"
    #         },
    #         "title2": "Select space for ocean tile",
    #         "options": [
    #             {
    #                 "title": "Standard projects"
    #             },
    #             {
    #                 "title": "Pass for this generation"
    #             },
    #             {
    #                 "title": {
    #                     "message": "Mollo"
    #                 }
    #             },
    #             {
    #                 "title": "Sell patents",
    #                 "cards": [
    #                     {
    #                         "name": "Testname1",
    #                         "calculatedCost": 15
    #                     }
    #                 ]
    #             }
    #         ]
    #     },
    #     "thisPlayer": {
    #         "megaCredits": 15
    #     }
    # }

    this_player = res["thisPlayer"]
    game = res["game"]
    # waiting_for = res["waitingFor"]
    protected_resources = this_player["protectedResources"]

    microbes = res["waitingFor"]["microbes"] if "waitingFor" in res and "microbes" in res["waitingFor"] else 0
    reserve_heat = protected_resources["heat"] if protected_resources["heat"] != "off" else 0
    reserve_mc = protected_resources["megacredits"] if protected_resources["megacredits"] != "off" else 0
    reserve_steel = protected_resources["steel"] if protected_resources["steel"] != "off" else 0
    reserve_titanium = protected_resources["titanium"] if protected_resources["titanium"] != "off" else 0

    plants_protected = np.zeros(1, dtype=np.int8) if this_player["protectedResources"]["plants"] == "off" else np.ones(
        1, dtype=np.int8)
    plant_production_protected = np.zeros(1, dtype=np.int8) if this_player["protectedProduction"][
                                                                   "plants"] == "off" else np.ones(1, dtype=np.int8)

    tags_dict = {
        "city": 0,
        "event": 1,
        "earth": 2,
        "plant": 3,
        "space": 4,
        "jovian": 5,
        "science": 6,
        "building": 7,
        "power": 8,
        "microbe": 9,
        "animal": 10
    }
    for tag in this_player["tags"]:
        tags_dict[tag["tag"]] = tag["count"]
    tags_array = list(tags_dict.values())

    is_action_option = "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase"

    available_action_options = np.zeros(NUMBER_ALL_ACTION_OPTIONS, dtype=np.int8)
    if is_action_option:
        for option in res["waitingFor"]["options"]:
            action_name = option["title"]["message"] if "message" in option["title"] else option["title"]
            index = ACTION_OPTIONS_NAME_INDEX[action_name]
            available_action_options[index] = 1
    else:
        available_action_options[ACTION_OPTIONS_NAME_INDEX["None"]] = 1

    selected_action_index = SELECTED_ACTION_OPTION_NAME_INDEX["None"]
    if "options" not in res["waitingFor"] or (
            "options" in res["waitingFor"] and res["waitingFor"]["title"] == "Initial Research Phase"):
        message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"]["title"] else \
            res["waitingFor"]["title"]
        selected_action_index = SELECTED_ACTION_OPTION_NAME_INDEX[message]

    available_cards = get_available_cards(res)

    available_project_cards = get_available_project_cards(res)

    available_cards_to_discard = get_available_cards_to_discard(res)

    available_cards_to_add_3_microbes_to = get_available_cards_to_add_3_microbes_to(res)

    available_cards_to_add_2_microbes_to = get_available_cards_to_add_2_microbes_to(res)

    available_cards_to_remove_2_animals_from = get_available_cards_to_remove_2_animals_from(res)

    available_cards_to_add_2_animals_to = get_available_cards_to_add_2_animals_to(res)

    available_cards_to_add_4_animals_to = get_available_cards_to_add_4_animals_to(res)

    available_cards_to_add_2_animals_to_2 = get_available_cards_to_add_2_animals_to_2(res)

    action_options = {}
    for option in ACTION_OPTIONS_NAME_INDEX.keys():
        action_options[option] = None
    if "options" in res["waitingFor"] and res["waitingFor"]["title"] != "Initial Research Phase":
        available_options = res["waitingFor"]["options"]
        for option in available_options:
            message = option["title"]["message"] if "message" in option["title"] else option["title"]
            action_options[message] = option

    selected_action = {}
    for action in SELECTED_ACTION_OPTION_NAME_INDEX.keys():
        selected_action[action] = None
    if "options" not in res["waitingFor"]:
        name = res["waitingFor"]["title"] if "message" not in res["waitingFor"]["title"] else res["waitingFor"]["title"]["message"]
        selected_action[name] = res["waitingFor"]

    observation = {
        AVAILABLE_ACTION_OPTIONS: available_action_options,
        SELECTED_ACTION_INDEX: build_discrete_i8(selected_action_index),
        AVAILABLE_CARDS: available_cards,
        AVAILABLE_PROJECT_CARDS: available_project_cards,
        AVAILABLE_CARDS_TO_DISCARD: available_cards_to_discard,
        AVAILABLE_CARDS_TO_ADD_3_MICROBES_TO: available_cards_to_add_3_microbes_to,
        AVAILABLE_CARDS_TO_ADD_2_MICROBES_TO: available_cards_to_add_2_microbes_to,
        AVAILABLE_CARDS_TO_REMOVE_2_ANIMALS_FROM: available_cards_to_remove_2_animals_from,
        AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO: available_cards_to_add_2_animals_to,
        AVAILABLE_CARDS_TO_ADD_4_ANIMALS_TO: available_cards_to_add_4_animals_to,
        AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO_2: available_cards_to_add_2_animals_to_2,
        AVAILABLE_HEAT: np.array([this_player["heat"]], dtype=np.int16),
        AVAILABLE_MC: np.array([this_player["megaCredits"]], dtype=np.int16),
        AVAILABLE_STEEL: np.array([this_player["steel"]], dtype=np.int16),
        AVAILABLE_TITANIUM: np.array([this_player["titanium"]], dtype=np.int16),
        AVAILABLE_MICROBES: np.array([microbes], dtype=np.int16),
        STEEL_VALUE: build_box_i8(this_player["steelValue"]),
        TITANIUM_VALUE: build_box_i8(this_player["titaniumValue"]),
        RESERVE_HEAT: build_box_i8(reserve_heat),
        RESERVE_MC: build_box_i8(reserve_mc),
        RESERVE_STEEL: build_box_i8(reserve_steel),
        RESERVE_TITANIUM: build_box_i8(reserve_titanium),
        AVAILABLE_SPACES: get_available_spaces(res),
        AVAILABLE_PLAYERS: get_available_players(res),
        PLAYED_CARDS_WITH_ACTIONS: get_available_cards_with_actions(res),
        AVAILABLE_MILESTONES: get_available_milestones(res),
        AVAILABLE_AWARDS: get_available_awards(res),
        AVAILABLE_STANDARD_PROJECTS: get_available_standard_projects(res),
        CORPORATION_TO_TAKE_FIRST_ACTION_OF: get_corporation_to_take_first_action_of(res),
        AMOUNT_OF_PLANTS_TO_REMOVE: get_amount_from_action_option(action_options["Remove ${0} plants from ${1}"], 0),
        PLAYER_TO_REMOVE_PLANTS_FROM: get_player_from_action_option(res, action_options["Remove ${0} plants from ${1}"],
                                                                    1),
        RESOURCE_TO_REMOVE: get_resource_to_remove(action_options["Remove ${0} ${1} from ${2}"]),
        AMOUNT_OF_RESOURCE_TO_REMOVE: get_amount_from_action_option(action_options["Remove ${0} ${1} from ${2}"], 1),
        PLAYER_TO_REMOVE_RESOURCE_FROM: get_player_from_action_option(res, action_options["Remove ${0} ${1} from ${2}"],
                                                                      2),
        AMOUNT_OF_MC_TO_STEAL: get_amount_from_action_option(action_options["Steal ${0} M€ from ${1}"], 0),
        PLAYER_TO_STEAL_MC_FROM: get_player_from_action_option(res, action_options["Steal ${0} M€ from ${1}"], 1),
        AMOUNT_OF_STEEL_TO_STEAL: get_amount_from_action_option(action_options["Steal ${0} steel from ${1}"], 0),
        PLAYER_TO_STEAL_STEEL_FROM: get_player_from_action_option(res, action_options["Steal ${0} steel from ${1}"], 1),
        AMOUNT_OF_MICROBES_TO_ADD: get_amount_from_action_option(action_options["Add ${0} microbes to ${1}"], 0),
        CARD_TO_ADD_MICROBES_TO: get_card_to_add_microbe_to(action_options["Add ${0} microbes to ${1}"], 1),
        WHAT_AWARD_TO_FUND: get_award_to_fund(action_options["Fund ${0} award"], 0),
        HOW_MANY_PLANTS_TO_CONVERT_INTO_GREENERY: get_amount_from_action_option(
            action_options["Convert ${0} plants into greenery"], 0),
        FUND_AWARD_COST: get_fund_award_cost(action_options["Fund an award (${0} M€)"], 0),  # 0 (none), 8, 14, 20
        TILE_TO_SELECT_SPACE_FOR: get_tile_to_select_space_for(selected_action["Select space for ${0} tile"], 0),
        PRODUCTION_TO_DECREASE: get_production_to_decrease(
            selected_action["Select player to decrease ${0} production by ${1} step(s)"], 0),
        STEPS_TO_DECREASE_PRODUCTION: get_amount_from_action_option(
            selected_action["Select player to decrease ${0} production by ${1} step(s)"], 1),
        WHAT_STANDARD_PROJECT_TO_SELECT_HOW_TO_PAY_FOR: get_standard_project_to_select_how_to_pay_for(
            selected_action["Select how to pay for the ${0} standard project"], 0),
        MAX_AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE: get_max_value(
            selected_action["Select amount of heat production to decrease"]),
        MAX_AMOUNT_OF_ENERGY_TO_SPEND: get_max_value(selected_action["Select amount of energy to spend"]),
        PASS_REMAINING_DRAFT_CARDS_TO_WHOM: get_player_from_action_option(res, selected_action[
            "Select a card to keep and pass the rest to ${0}"], 0),
        AVAILABLE_CORPORATIONS: get_available_corporations(res),
        ACTIONS_TAKEN_THIS_ROUND: build_box_i8(this_player[ACTIONS_TAKEN_THIS_ROUND]),
        AVAILABLE_BLUE_CARD_ACTION_COUNT: build_box_i8(this_player[AVAILABLE_BLUE_CARD_ACTION_COUNT]),
        CARDS_IN_HAND_NUMBER: build_box_i8(this_player[CARDS_IN_HAND_NUMBER]),
        CITIES_COUNT: build_box_i8(this_player[CITIES_COUNT]),
        AVAILABLE_ENERGY: np.array([this_player["energy"]], dtype=np.int16),
        ENERGY_PRODUCTION: build_box_i8(this_player[ENERGY_PRODUCTION]),
        HEAT_PRODUCTION: build_box_i8(this_player[HEAT_PRODUCTION]),
        MEGA_CREDIT_PRODUCTION: build_box_i8(this_player[MEGA_CREDIT_PRODUCTION]),
        AVAILABLE_PLANTS: np.array([this_player[AVAILABLE_PLANTS]], dtype=np.int16),
        PLANT_PRODUCTION: build_box_i8(this_player[PLANT_PRODUCTION]),
        PLANTS_PROTECTED: plants_protected,
        PLANT_PRODUCTION_PROTECTED: plant_production_protected,
        STEEL_PRODUCTION: build_box_i8(this_player[STEEL_PRODUCTION]),
        TAGS: np.array(tags_array, dtype=np.int8),
        TERRAFORM_RATING: np.array([this_player[TERRAFORM_RATING]], dtype=np.int16),
        TITANIUM_PRODUCTION: build_box_i8(this_player[TITANIUM_PRODUCTION]),
        TOTAL_VICTORY_POINTS: np.array([this_player["victoryPointsBreakdown"]["total"]], dtype=np.int16),
        PICKED_CORPORATION: get_picked_corporation(res),
        CARDS_IN_HAND: get_cards_in_hand(res),
        DEALT_CARDS: get_dealt_cards(res),
        GENERATION: build_box_i8(game[GENERATION]),
        OXYGEN_LEVEL: build_box_i8(game[OXYGEN_LEVEL]),
        TEMPERATURE: build_box_i8(game[TEMPERATURE]),
        CURRENT_PHASE: build_box_i8(get_current_phase(res)),
        OCCUPIED_SPACES: get_occupied_spaces(res),
    }
    return observation
