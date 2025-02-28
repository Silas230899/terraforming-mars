import json

from AiPlayer import initial_research_phase, research_phase, draft, turn, create_game
from Player import Player


class ClientGame:
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    def __init__(self, http_connection):
        self.http_connection = http_connection

        new_game = create_game(http_connection)

        self.player1 = Player(new_game["players"][0]["color"],
                              new_game["players"][0]["id"],
                              new_game["players"][0]["name"])
        self.player2 = Player(new_game["players"][1]["color"],
                              new_game["players"][1]["id"],
                              new_game["players"][1]["name"])
        self.player3 = Player(new_game["players"][2]["color"],
                              new_game["players"][2]["id"],
                              new_game["players"][2]["name"])

    def start(self):
        res = initial_research_phase(self.player1, self.http_connection)

        initial_research_phase(self.player2, self.http_connection)
        #print(json.dumps(res, indent=2))
        exit(-1)
        res = initial_research_phase(self.player3, self.http_connection)

        while True:
            res = self.generation(res)
            if res is None:
                break

    # wenn man normal dran ist ist man active und die anderen nicht, im draft wenn quasi alle dran sind ist man selbst nicht active
    def get_next_player(self, players):
        for player in players:
            if player["isActive"]:
                if self.player1.name == player["name"]:
                    return self.player1
                elif self.player2.name == player["name"]:
                    return self.player2
                elif self.player3.name == player["name"]:
                    return self.player3

    def generation(self, res):
        current_player = self.get_next_player(res["players"])

        if res["game"]["phase"] != "action" and res["game"]["phase"] != "preludes":
            print("phase should be 'action' or 'preludes' but is " + str(res["game"]["phase"]))
            exit(-1)

        while res["game"]["phase"] == "action" or res["game"]["phase"] == "production" or res["game"]["phase"] == "preludes":
            old_res = res
            res = turn(current_player, self.http_connection)
            if "players" not in res:
                print("run id: " + old_res["runId"])
                print("player id: " + old_res["id"])
                print("Players not in res:")
                print("old res:")
                print(old_res)
                print(res)
                exit(-1)

            current_player = self.get_next_player(res["players"])

        if res["game"]["phase"] == "drafting":
            res = turn(self.player1, self.http_connection)
            res = turn(self.player2, self.http_connection)
            res = turn(self.player3, self.http_connection)

            res = turn(self.player1, self.http_connection)
            res = turn(self.player2, self.http_connection)
            res = turn(self.player3, self.http_connection)

            res = turn(self.player1, self.http_connection)
            res = turn(self.player2, self.http_connection)
            res = turn(self.player3, self.http_connection)
        elif res["game"]["phase"] == "end":
            for player in res["players"]:
                pass
                #print(player["name"] + ": " + str(player["victoryPointsBreakdown"]["total"]) + ", ", end="")
            return None
        else:
            print("phase should be 'drafting' but is " + str(res["game"]["phase"]))
            exit(-1)

        if res["game"]["phase"] == "research":
            res = turn(self.player1, self.http_connection)
            while "waitingFor" in res and res["game"]["phase"] == "research":
                res = turn(self.player1, self.http_connection)
            res = turn(self.player2, self.http_connection)
            while "waitingFor" in res and res["game"]["phase"] == "research":
                res = turn(self.player2, self.http_connection)
            res = turn(self.player3, self.http_connection)
            while "waitingFor" in res and res["game"]["phase"] == "research":
                res = turn(self.player3, self.http_connection)
        else:
            print("phase should be 'research' but is " + str(res["game"]["phase"]))
            exit(-1)

        return res