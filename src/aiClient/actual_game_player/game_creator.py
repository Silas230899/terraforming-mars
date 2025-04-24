import http.client
import json

from ai_player.network_related import create_game
from ai_player.tfm_settings import settings

if __name__ == '__main__':
    http_connection = http.client.HTTPConnection("localhost", 8080)

    result = create_game(http_connection, json.dumps(settings))

    for player in result["players"]:
        print("Player ", player["name"], player["id"], player["color"])