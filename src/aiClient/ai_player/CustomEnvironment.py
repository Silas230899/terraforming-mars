import http.client
import json
import math

import gymnasium as gym
from gymnasium import spaces
import random

from gymnasium.spaces import Box, Discrete, MultiBinary
from numpy import argmax

from ai_player.HybridActionWrapper import HybridActionWrapper
from ai_player.ppo_stuff import ppo
from Player import Player
from ai_player.tfm_settings import settings
from network_related import *
from observation_creation import *


class CustomEnv(gym.Env):
    http_connection = None

    player1: Player = None
    player2: Player = None
    player3: Player = None

    observed_player: Player = None
    res_of_observed_player = None

    run_id = -1

    policy_model: ppo.PPO
    action_wrapper: HybridActionWrapper

    def __init__(self):
        super(CustomEnv, self).__init__()

        self.http_connection = http.client.HTTPConnection("localhost", 8080)

        # Beobachtungsraum
        self.observation_space = spaces.Dict({
            AVAILABLE_ACTION_OPTIONS: MultiBinary(NUMBER_ALL_ACTION_OPTIONS),
            SELECTED_ACTION_INDEX: Discrete(NUMBER_ALL_ACTIONS),
            AVAILABLE_CARDS: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_PROJECT_CARDS: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_DISCARD: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_ADD_3_MICROBES_TO: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_ADD_2_MICROBES_TO: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_REMOVE_2_ANIMALS_FROM: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_ADD_4_ANIMALS_TO: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_CARDS_TO_ADD_2_ANIMALS_TO_2: MultiBinary(NUMBER_OF_CARDS),

            AVAILABLE_HEAT: Box(0, 500, (1,), np.int16),
            AVAILABLE_MC: Box(0, 500, (1,), np.int16),
            AVAILABLE_STEEL: Box(0, 500, (1,), np.int16),
            AVAILABLE_TITANIUM: Box(0, 500, (1,), np.int16),
            AVAILABLE_MICROBES: Box(0, 500, (1,), np.int16),
            STEEL_VALUE: Box(0, 3, (1,), np.int8),
            TITANIUM_VALUE: Box(0, 3, (1,), np.int8),
            RESERVE_HEAT: Box(0, 50, (1,), np.int8),
            RESERVE_MC: Box(0, 50, (1,), np.int8),
            RESERVE_STEEL: Box(0, 50, (1,), np.int8),
            RESERVE_TITANIUM: Box(0, 50, (1,), np.int8),
            AVAILABLE_SPACES: MultiBinary(NUMBER_SPACES),
            AVAILABLE_PLAYERS: MultiBinary(NUMBER_PLAYERS),
            PLAYED_CARDS_WITH_ACTIONS: MultiBinary(NUMBER_OF_CARDS),
            AVAILABLE_MILESTONES: MultiBinary(len(MILESTONES_STR_INT)),
            AVAILABLE_AWARDS: MultiBinary(len(AWARDS_STR_INT)),
            AVAILABLE_STANDARD_PROJECTS: MultiBinary(len(STANDARD_PROJECTS_INDEX_NAME)),

            # for "Take first action of ${0} corporation"
            CORPORATION_TO_TAKE_FIRST_ACTION_OF: Discrete(len(CORPORATIONS_WITH_FIRST_ACTION)),

            # "Remove ${0} plants from ${1}"
            AMOUNT_OF_PLANTS_TO_REMOVE: Box(0, 8, (1,), np.int8),
            PLAYER_TO_REMOVE_PLANTS_FROM: Discrete(NUMBER_PLAYERS),

            # "Remove ${0} ${1} from ${2}"
            RESOURCE_TO_REMOVE: Discrete(len(REMOVABLE_RESOURCES_NAMES)),
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
            CARD_TO_ADD_MICROBES_TO: Discrete(len(CARDS_MICROBES_CAN_BE_ADDED_TO)),

            # "Fund ${0} award"
            WHAT_AWARD_TO_FUND: Discrete(len(AWARDS_STR_INT)),

            # Convert ${0} plants into greenery
            HOW_MANY_PLANTS_TO_CONVERT_INTO_GREENERY: Box(0, 8, (1,), np.int8),

            # Fund an award (${0} M€)
            FUND_AWARD_COST: Discrete(4),  # none, 8, 14, 20

            # Select space for ${0} tile
            TILE_TO_SELECT_SPACE_FOR: Discrete(len(TILE_NAMES_OF_SELECTABLE_SPACES)),

            # Select player to decrease ${0} production by ${1} step(s)
            PRODUCTION_TO_DECREASE: Discrete(len(DECREASABLE_PRODUCTIONS_NAMES)),
            STEPS_TO_DECREASE_PRODUCTION: Box(0, 8, (1,), np.int8),

            # Select how to pay for the ${0} standard project
            WHAT_STANDARD_PROJECT_TO_SELECT_HOW_TO_PAY_FOR: Discrete(len(STANDARD_PROJECTS_NAME_INDEX)),

            # Select amount of heat production to decrease
            MAX_AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE: Box(0, 50, (1,), np.int8),

            # Select amount of energy to spend
            MAX_AMOUNT_OF_ENERGY_TO_SPEND: Box(0, 50, (1,), np.int8),

            # Select a card to keep and pass the rest to ${0}
            PASS_REMAINING_DRAFT_CARDS_TO_WHOM: Discrete(NUMBER_PLAYERS),

            # Initial Research Phase
            AVAILABLE_CORPORATIONS: MultiBinary(NUMBER_OF_CORPORATIONS),

            # others
            ACTIONS_TAKEN_THIS_ROUND: Box(0, 127, (1,), np.int8),
            AVAILABLE_BLUE_CARD_ACTION_COUNT: Box(0, 127, (1,), np.int8),
            CARDS_IN_HAND_NUMBER: Box(0, 127, (1,), np.int8),
            CITIES_COUNT: Box(0, 127, (1,), np.int8),
            AVAILABLE_ENERGY: Box(0, 500, (1,), np.int16),
            ENERGY_PRODUCTION: Box(0, 127, (1,), np.int8),
            HEAT_PRODUCTION: Box(0, 127, (1,), np.int8),
            MEGA_CREDIT_PRODUCTION: Box(0, 127, (1,), np.int8),
            AVAILABLE_PLANTS: Box(0, 500, (1,), np.int16),
            PLANT_PRODUCTION: Box(0, 127, (1,), np.int8),
            PLANTS_PROTECTED: MultiBinary(1),
            PLANT_PRODUCTION_PROTECTED: MultiBinary(1),
            STEEL_PRODUCTION: Box(0, 127, (1,), np.int8),
            TAGS: Box(0, 127, (11,), np.int8),
            # city, event, earth, plant, space, jovia, science, building, power, microbe, animal
            TERRAFORM_RATING: Box(0, 511, (1,), np.int16),
            TITANIUM_PRODUCTION: Box(0, 127, (1,), np.int8),
            TOTAL_VICTORY_POINTS: Box(0, 511, (1,), np.int16),
            PICKED_CORPORATION: Discrete(NUMBER_CORPORATIONS_DISCRETE),  # last is none
            CARDS_IN_HAND: MultiBinary(len(CARD_NAMES_INT_STR)),
            DEALT_CARDS: MultiBinary(len(CARD_NAMES_INT_STR)),
            GENERATION: Box(0, 127, (1,), np.int8),
            OXYGEN_LEVEL: Box(0, 127, (1,), np.int8),
            TEMPERATURE: Box(-30, 100, (1,), np.int8),
            CURRENT_PHASE: Discrete(len(PHASES_STR_INT)),
            OCCUPIED_SPACES: spaces.MultiDiscrete(np.full((NUMBER_SPACES,), 4, np.int8))
        })

        self.action_space = spaces.Dict({
            SELECTED_ACTION_OPTION_INDEX: Discrete(NUMBER_ALL_ACTION_OPTIONS),
            SELECTED_CARD_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_PROJECT_CARD_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_DISCARD_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_ADD_3_MICROBES_TO_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_ADD_2_MICROBES_TO_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_REMOVE_2_ANIMALS_FROM_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_ADD_2_ANIMALS_TO_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_ADD_4_ANIMALS_TO_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_CARD_TO_ADD_2_ANIMALS_TO_2_INDEX: Discrete(NUMBER_OF_CARDS),

            PAY_HEAT_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MC_PERCENTAGE: Box(low=0, high=1, shape=(1,), dtype=np.float32),
            PAY_STEEL_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_TITANIUM_PERCENTAGE: Box(0, 1, (1,), np.float32),
            PAY_MICROBES_PERCENTAGE: Box(0, 1, (1,), np.float32),
            MULTIPLE_SELECTED_CARDS: MultiBinary(NUMBER_OF_CARDS),
            SELECTED_SPACE_INDEX: Discrete(NUMBER_SPACES),
            SELECTED_PLAYER: Discrete(NUMBER_PLAYERS),
            SELECTED_CARD_WITH_ACTION_INDEX: Discrete(NUMBER_OF_CARDS),
            SELECTED_MILESTONE_INDEX: Discrete(len(MILESTONES_STR_INT)),
            SELECTED_AWARD_INDEX: Discrete(len(AWARDS_STR_INT)),
            SELECTED_STANDARD_PROJECT_INDEX: Discrete(len(STANDARD_PROJECTS_NAME_INDEX)),

            # Select 2 card(s) to keep
            TWO_SELECTED_CARDS_INDICES: MultiBinary(NUMBER_OF_CARDS),

            # Select amount of heat production to decrease
            AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE: Box(0, 50, (1,), np.int8),

            # Select amount of energy to spend
            AMOUNT_OF_ENERGY_TO_SPEND: Box(0, 50, (1,), np.int8),

            # Select card(s) to buy
            MULTIPLE_SELECTED_RESEARCH_CARDS: MultiBinary(NUMBER_OF_CARDS),
            DONT_BUY_CARD: Discrete(2),  # zero means no, one means yes

            # Initial Research Phase
            SELECTED_CORPORATION: Discrete(NUMBER_OF_CORPORATIONS),
        })

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
                    case _:
                        print("error getting current player")
                        exit(-1)


    def play_all_at_once(self, res_player1, res_player2, res_player3):
        observation_player1 = create_observation_from_res(res_player1)
        observation_player2 = create_observation_from_res(res_player2)
        observation_player3 = create_observation_from_res(res_player3)

        # weil die ergebnisse der spieler nicht voneinander abhängen ist die reihenfolge hier beliebig
        match self.observed_player:
            case self.player1:
                # calc player 2 and 3 now
                action_player2, _ = self.policy_model.predict(observation_player2)
                action_player2 = self.action_wrapper.action(action_player2)
                _ = self.normal_turn(action_player2, res_player2, self.player2)
                action_player3, _ = self.policy_model.predict(observation_player3)
                action_player3 = self.action_wrapper.action(action_player3)
                _ = self.normal_turn(action_player3, res_player3, self.player3)
                return observation_player1, res_player1
            case self.player2:
                # calc player 1 and 3 now
                action_player1, _ = self.policy_model.predict(observation_player1)
                action_player1 = self.action_wrapper.action(action_player1)
                _ = self.normal_turn(action_player1, res_player1, self.player1)
                action_player3, _ = self.policy_model.predict(observation_player3)
                action_player3 = self.action_wrapper.action(action_player3)
                _ = self.normal_turn(action_player3, res_player3, self.player3)
                return observation_player2, res_player2
            case self.player3:
                action_player1, _ = self.policy_model.predict(observation_player1)
                action_player1 = self.action_wrapper.action(action_player1)
                _ = self.normal_turn(action_player1, res_player1, self.player1)
                action_player2, _ = self.policy_model.predict(observation_player2)
                action_player2 = self.action_wrapper.action(action_player2)
                _ = self.normal_turn(action_player2, res_player2, self.player2)
                return observation_player3, res_player3


    def reset(self, seed=None, options=None):
        super().reset()

        result = create_game(self.http_connection, json.dumps(settings))

        self.player1 = None
        self.player2 = None
        self.player3 = None

        self.player1 = Player(result["players"][0]["color"],
                              result["players"][0]["id"],
                              result["players"][0]["name"])
        self.player2 = Player(result["players"][1]["color"],
                              result["players"][1]["id"],
                              result["players"][1]["name"])
        self.player3 = Player(result["players"][2]["color"],
                              result["players"][2]["id"],
                              result["players"][2]["name"])

        res_player1 = get_game(self.http_connection, self.player1.id)
        res_player2 = get_game(self.http_connection, self.player2.id)
        res_player3 = get_game(self.http_connection, self.player3.id)

        self.run_id = res_player1["runId"]  # all players have the same run_id

        self.observed_player = random.choice([self.player1, self.player2, self.player3])

        # für rot: gelb links, grün rechts
        # für grün: rot links, gelb rechts
        # für gelb: grün links, rot rechts

        observation, self.res_of_observed_player = self.play_all_at_once(res_player1, res_player2, res_player3)
        return observation, {}


    def step(self, action):
        # action ausführen
        res = self.normal_turn(action, self.res_of_observed_player, self.observed_player) # this is from observed player
        #print(res)
        if res["game"]["phase"] == "drafting":
            res_player1 = get_game(self.http_connection, self.player1.id)
            res_player2 = get_game(self.http_connection, self.player2.id)
            res_player3 = get_game(self.http_connection, self.player3.id)

            return_obs, self.res_of_observed_player = self.play_all_at_once(res_player1, res_player2, res_player3)

            reward = 1
            done = False
            return return_obs, reward, done, False, {}
        else:
            next_player = self.get_current_player(res["players"]) # herausfinden, wer als nächstes dran ist

            while next_player != self.observed_player:
                # die anderen spieler spielen
                res = get_game(self.http_connection, next_player.id)
                observation_other_player = create_observation_from_res(res)
                action_other_player, _ = self.policy_model.predict(observation_other_player)
                res = self.normal_turn(action_other_player, res, next_player)
                next_player = self.get_current_player(res["players"]) # herausfinden, wer als nächstes dran ist

            # now next_player == self.observed_player:
            res = get_game(self.http_connection, next_player.id)
            observation = create_observation_from_res(res)
            self.res_of_observed_player = res

        reward = np.random.random()
        done = res["game"]["phase"] == "end"

        return observation, reward, done, False, {}


    def normal_turn(self, action, res, which_player):

        this_player_color = res["thisPlayer"]["color"]

        payload = None

        run_id = self.run_id

        if "options" in res["waitingFor"]:
            # this has to be handled separately bc the options are not really options but all mandatory
            if res["waitingFor"]["title"] == "Initial Research Phase":
                selected_corporation_name = ALL_CORPORATIONS_INDEX_NAME[action[SELECTED_CORPORATION]]

                #print(json.dumps(res["waitingFor"],indent=2))
                available_cash_for_project_cards = CORPORATIONS_STARTING_MC[selected_corporation_name]

                available_cards = res["waitingFor"]["options"][2]["cards"]
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
                        most_expensive_card_index = argmax(
                            map(lambda card: card["calculatedCost"], selected_project_cards))
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

                payload = create_initial_cards_card_card_card_response(run_id, selected_corporation_name,
                                                                       selected_prelude_cards_names,
                                                                       selected_project_card_names)
                #print(json.dumps(payload, indent=2))
                #print(json.dumps(payload, indent=2))
            else:  # wenn optionen ganz normal tatsächlich optionen sind
                available_options = res["waitingFor"]["options"]

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

                action_name = selected_option["title"]["message"] if "message" in selected_option["title"] else \
                selected_option["title"]
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
                          "Take first action of ${0} corporation",  # c = which_option["title"]["data"][0]["value"]
                          "Remove ${0} plants from ${1}",
                          "Remove ${0} ${1} from ${2}",
                          "Steal ${0} M€ from ${1}",
                          "Steal ${0} steel from ${1}",
                          "Add ${0} microbes to ${1}",
                          "Add resource to card ${0}",
                          "Add ${0} animals to ${1}",
                          "Fund ${0} award"):
                        payload = create_or_resp_option(run_id, selected_option_index)
                    case "Play project card":
                        available_cards = selected_option["cards"]
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_PROJECT_CARD_INDEX]]
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
                            for p in res["players"]:
                                if p["color"] == which_player.color:
                                    for card in p["tableau"]:
                                        if card["name"] == "Psychrophiles":
                                            can_pay_with_microbes = True
                                            break
                                    break

                        pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes = calc_payment_for_project_card(action,
                                                                                                                res,
                                                                                                                card_cost,
                                                                                                                can_pay_with_heat,
                                                                                                                can_pay_with_steel,
                                                                                                                can_pay_with_titanium,
                                                                                                                can_pay_with_microbes,
                                                                                                                reserve_heat,
                                                                                                                reserve_mc,
                                                                                                                reserve_titanium,
                                                                                                                reserve_steel)

                        payload = create_or_resp_project_card_payment(run_id, selected_option_index, card_name,
                                                                      pay_heat, pay_mc, pay_steel, pay_titanium,
                                                                      pay_microbes)
                    case "Sell patents":  # multiple cards
                        selected_project_cards = []
                        selected_card_indices = action[MULTIPLE_SELECTED_CARDS]
                        for idx, binary in enumerate(selected_card_indices):
                            if binary == 1:
                                selected_card_name: str = CARD_NAMES_INT_STR[idx]
                                selected_project_cards.append(selected_card_name)
                        payload = create_or_resp_card_cards(run_id, selected_option_index, selected_project_cards)
                    case "Perform an action from a played card":
                        available_cards = selected_option["cards"]
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_WITH_ACTION_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Select a card to discard":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_TO_DISCARD_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Add 3 microbes to a card":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_ADD_3_MICROBES_TO_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Select card to add 2 microbes":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_ADD_2_MICROBES_TO_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Select card to remove 2 Animal(s)":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_REMOVE_2_ANIMALS_FROM_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Select card to add 2 animals":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_ADD_2_ANIMALS_TO_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Select card to add 4 animals":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_ADD_4_ANIMALS_TO_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case "Add 2 animals to a card":
                        selected_card_from_all_name: str = CARD_NAMES_INT_STR[
                            action[SELECTED_CARD_TO_ADD_2_ANIMALS_TO_2_INDEX]]
                        payload = create_or_resp_card_cards(run_id, selected_option_index,
                                                            [selected_card_from_all_name])
                    case ("Select space for greenery tile",
                          "Convert ${0} plants into greenery"):
                        available_spaces_ids = selected_option["spaces"]
                        selected_space_index = action[SELECTED_SPACE_INDEX]
                        selected_space_id = str(
                            selected_space_index + 1)  # TODO maybe "1" is not treated the same as "01"
                        payload = create_or_resp_space_space_id(run_id, selected_option_index, selected_space_id)
                    case "Select adjacent player to remove 4 M€ from":
                        available_players_colors = selected_option["players"]
                        selected_player_index = action[SELECTED_PLAYER]
                        selected_player_color = get_color_of_player_index_by_current_player_color(selected_player_index,
                                                                                                  this_player_color)
                        payload = create_or_resp_player_player(run_id, selected_option_index, selected_player_color)
                    case "Fund an award (${0} M€)":
                        available_awards = selected_option["options"]
                        selected_award_from_all_name: str = AWARDS_INT_STR[action[SELECTED_AWARD_INDEX]]
                        selected_award_index = -1
                        for idx, award in enumerate(available_awards):
                            if award["title"] == selected_award_from_all_name:
                                selected_award_index = idx
                                break
                        payload = create_or_resp_or_resp_option(run_id, selected_option_index, selected_award_index)
                    case "Standard projects":
                        # wenn das SP nicht verfügbar ist, darf es gar nicht erst als option im beobachtungsraum sein
                        selected_standard_project_name = STANDARD_PROJECTS_INDEX_NAME[
                            action[SELECTED_STANDARD_PROJECT_INDEX]]
                        create_or_resp_card_cards(run_id, selected_option_index, [selected_standard_project_name])
                    case "Claim a milestone":
                        available_milestones = selected_option["options"]
                        selected_milestone_from_all_name: str = MILESTONES_INT_STR[action[SELECTED_MILESTONE_INDEX]]
                        selected_milestone_index = -1
                        for idx, milestone in enumerate(available_milestones):
                            if milestone["title"] == selected_milestone_from_all_name:
                                selected_milestone_index = idx
                                break
                        create_or_resp_or_resp_option(run_id, selected_option_index, selected_milestone_index)
        else:
            message = res["waitingFor"]["title"]["message"] if "message" in res["waitingFor"][
                "title"] else res["waitingFor"]["title"]
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
                    selected_space_index_from_all = action[SELECTED_SPACE_INDEX]
                    selected_space_id = str(selected_space_index_from_all + 1)
                    payload = create_space_id_response(run_id, selected_space_id)
                case "Select player to decrease ${0} production by ${1} step(s)":
                    selected_player_index = action[SELECTED_PLAYER]
                    selected_player_color = get_color_of_player_index_by_current_player_color(selected_player_index,
                                                                                              this_player_color)
                    payload = create_player_response(run_id, selected_player_color)
                case ("Select card to add ${0} ${1}",  # geschenkt
                      "Select builder card to copy",
                      "Select 1 card(s) to keep",
                      "Select card to remove 1 Microbe(s)",
                      "Select card to remove 1 Animal(s)",
                      "Select prelude card to play",
                      "Select a card to keep and pass the rest to ${0}"):
                    available_cards = res["waitingFor"]["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_CARD_INDEX]]
                    payload = create_cards_response(run_id, [selected_card_from_all_name])
                case "Select card(s) to buy":  # 0 or 1
                    available_cards = res["waitingFor"]["cards"]
                    max_amount_of_cards = res["waitingFor"]["max"]
                    if max_amount_of_cards == 1:
                        selected_cards_names = []
                        if action[DONT_BUY_CARD] == 1:
                            selected_card_index = action[SELECTED_CARD_INDEX]
                            selected_card_from_all_name: str = CARD_NAMES_INT_STR[selected_card_index]
                            selected_cards_names = [selected_card_from_all_name]
                        elif action[DONT_BUY_CARD] == 0:
                            pass
                        payload = create_cards_response(run_id, selected_cards_names)
                    elif max_amount_of_cards == 4:
                        selected_cards_names = []
                        selected_card_indices = action[MULTIPLE_SELECTED_RESEARCH_CARDS]
                        for idx, binary in enumerate(selected_card_indices):
                            if binary == 1:
                                selected_card_name: str = CARD_NAMES_INT_STR[idx]
                                selected_cards_names.append(selected_card_name)
                        payload = create_cards_response(run_id, selected_cards_names)
                case "Select 2 card(s) to keep":
                    available_cards = res["waitingFor"]["cards"]
                    selected_cards_indices = action[TWO_SELECTED_CARDS_INDICES]
                    selected_cards_names = []
                    for idx, binary in enumerate(selected_cards_indices):
                        if binary == 1:
                            selected_card_name: str = CARD_NAMES_INT_STR[idx]
                            selected_cards_names.append(selected_card_name)

                    if len(selected_cards_names) != 2:
                        print("did not correctly select 2 cards")
                        exit(-458764)
                    create_cards_response(run_id, selected_cards_names)
                case "You cannot afford any cards":
                    create_cards_response(run_id, [])
                case "Play project card":
                    available_cards = res["waitingFor"]["cards"]
                    selected_card_from_all_name: str = CARD_NAMES_INT_STR[action[SELECTED_PROJECT_CARD_INDEX]]
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

                    payment_options = res["waitingFor"]["paymentOptions"]
                    can_pay_with_heat = payment_options["heat"]
                    can_pay_with_steel = card_name in BUILDING_CARDS_SET  # building cards
                    can_pay_with_titanium = card_name in SPACE_CARDS_SET  # space cards
                    can_pay_with_microbes = False
                    if card_name in PLANT_CARDS_SET:
                        for p in res["players"]:
                            if p["color"] == which_player.color:
                                for card in p["tableau"]:
                                    if card["name"] == "Psychrophiles":
                                        can_pay_with_microbes = True
                                        break
                                break

                    pay_heat, pay_mc, pay_steel, pay_titanium, pay_microbes = calc_payment_for_project_card(action,
                                                                                                            res,
                                                                                                            card_cost,
                                                                                                            can_pay_with_heat,
                                                                                                            can_pay_with_steel,
                                                                                                            can_pay_with_titanium,
                                                                                                            can_pay_with_microbes,
                                                                                                            reserve_heat,
                                                                                                            reserve_mc,
                                                                                                            reserve_titanium,
                                                                                                            reserve_steel)

                    create_project_card_payment_response(run_id, card_name, pay_heat, pay_mc, pay_steel, pay_titanium,
                                                         pay_microbes)
                    pass
                case ("Select how to pay for the ${0} standard project",
                      "Select how to spend ${0} M€",
                      "Select how to spend ${0} M€ for ${1} cards",
                      "Select how to pay for ${0} action",  # too complicated
                      "Select how to pay for award",
                      "Select how to pay for action",
                      "Select how to pay for milestone"):

                    cost = res["waitingFor"]["amount"]

                    payment_options = res["waitingFor"]["paymentOptions"]
                    can_pay_with_heat = payment_options["heat"]
                    can_pay_with_titanium = payment_options["titanium"]
                    can_pay_with_steel = payment_options["steel"]

                    pay_heat, pay_mc, pay_steel, pay_titanium, _ = calc_payment_for_project_card(action,
                                                                                                 res,
                                                                                                 cost,
                                                                                                 can_pay_with_heat,
                                                                                                 can_pay_with_steel,
                                                                                                 can_pay_with_titanium,
                                                                                                 False,
                                                                                                 0,
                                                                                                 0,
                                                                                                 0,
                                                                                                 0)
                    payload = create_payment_response(run_id, pay_heat, pay_mc, pay_steel, pay_titanium)
                case "Select amount of heat production to decrease":
                    selected_amount = action[AMOUNT_OF_HEAT_PRODUCTION_TO_DECREASE]
                    # min = current_state["waitingFor"]["min"]
                    max = res["waitingFor"]["max"]
                    amount = min(selected_amount, max)
                    payload = create_amount_response(run_id, amount)
                case "Select amount of energy to spend":
                    selected_amount = action[AMOUNT_OF_ENERGY_TO_SPEND]
                    max = res["waitingFor"]["max"]
                    amount = min(selected_amount, max)
                    payload = create_amount_response(run_id, amount)

        res = send_player_input(self.http_connection, which_player.id, payload)
        # from this res create new observation

        # send_player_input(json.dumps(select_space_data), player.id, http_connection)
        return res


def calc_payment_for_project_card(action,
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