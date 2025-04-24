import json
import http.client

def create_game(http_connection, payload):
    http_connection.request("PUT", "/game", body=payload)
    response = http_connection.getresponse()
    result = json.loads(response.read().decode())
    return result


def get_waiting_for(http_connection, player_id, game_age, undo_count):
    http_connection.request("GET", "/api/waitingfor?id=" + player_id + "&gameAge=" + str(game_age) + "&undoCount=" + str(undo_count))
    response = http_connection.getresponse()
    return json.loads(response.read().decode())

def send_player_input(http_connection: http.client.HTTPConnection, player_id, payload):
    payload = json.dumps(payload)
    http_connection.request("POST", "/player/input?id=" + player_id, body=payload)
    response = http_connection.getresponse()
    result = json.loads(response.read().decode())
    return result


def get_game(http_connection, player_id):
    http_connection.request("GET", "/api/player?id=" + player_id)
    response = http_connection.getresponse()
    return json.loads(response.read().decode())


def create_or_resp_option(run_id, index):
    return {
        "runId": run_id,
        "type": "or",
        "index": index,
        "response": {
            "type": "option"
        }
    }


def create_initial_cards_card_card_card_response(run_id, corporation_card_name, prelude_cards_names,
                                                 project_cards_names):
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


def create_or_resp_project_card_payment(run_id, index, card_name, heat, mc, steel, titanium, microbes):
    return {
        "runId": run_id,
        "type": "or",
        "index": index,
        "response": {
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
    }


def create_or_resp_card_cards(run_id, index, card_names):
    return {
        "runId": run_id,
        "type": "or",
        "index": index,
        "response": {
            "type": "card",
            "cards": card_names
        }
    }


def create_space_id_response(run_id, selected_space):
    return {
        "runId": run_id,
        "type": "space",
        "spaceId": selected_space
    }


def create_or_resp_space_space_id(run_id, index, selected_space):
    return {
        "runId": run_id,
        "type": "or",
        "index": index,
        "response": {
            "type": "space",
            "spaceId": selected_space
        }
    }


def create_or_resp_player_player(run_id, index, selected_player):
    return {
        "runId": run_id,
        "type": "or",
        "index": index,
        "response": {
            "type": "player",
            "player": selected_player
        }
    }


def create_or_resp_or_resp_option(run_id, action_index, index2):
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


def create_player_response(run_id, selected_player):
    return {
        "runId": run_id,
        "type": "player",
        "player": selected_player
    }


def create_cards_response(run_id, selected_cards_names):
    return {
        "runId": run_id,
        "type": "card",
        "cards": selected_cards_names
    }


def create_payment_response(run_id, heat, mc, steel, titanium):
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


def create_amount_response(run_id, amount):
    return {
        "runId": run_id,
        "type": "amount",
        "amount": amount
    }


def create_project_card_payment_response(run_id, card_name, heat, mc, steel, titanium, microbes):
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
    return select_card_data
