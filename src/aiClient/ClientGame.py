from AiPlayer import Player, initial_research_phase, research_phase, draft, turn, create_game


class ClientGame:
    http_connection = None

    player1 = None
    player2 = None
    player3 = None

    def __init__(self, http_connection):
        self.http_connection = http_connection

        new_game = create_game()

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
        initial_research_phase(self.player1)
        initial_research_phase(self.player2)
        res = initial_research_phase(self.player3)

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
        #print("Generation " + str(res["game"]["generation"]))
        current_player = self.get_next_player(res["players"])

        if res["game"]["phase"] != "action":
            print("phase should be 'action' but is " + str(res["game"]["phase"]))
            #print(res)
            exit(-1)

        while res["game"]["phase"] == "action" or res["game"]["phase"] == "production":
            if "waitingFor" in res:
                pass
                #print("waiting for something")
            else:
                pass
                #print("not waiting for something")

            old_res = res
            res = turn(current_player)
            if "players" not in res:
                print("Players not in res:")
                print("old res:")
                print(old_res)
                print(res)
                exit(-1)

            current_player = self.get_next_player(res["players"])

        if res["game"]["phase"] == "drafting":
            draft(self.player1)
            draft(self.player2)
            draft(self.player3)

            draft(self.player1)
            draft(self.player2)
            draft(self.player3)

            draft(self.player1)
            draft(self.player2)
            res = draft(self.player3)
        elif res["game"]["phase"] == "end":
            print("The game has ended ", end="")
            #print(res)
            for player in res["players"]:
                print(player["name"] + ": " + str(player["victoryPointsBreakdown"]["total"]) + ", ", end="")
            #exit(0)
            print()
            return None
        else:
            print("phase should be 'drafting' but is " + str(res["game"]["phase"]))
            exit(-1)

        if res["game"]["phase"] == "research":
            research_phase(self.player1)
            research_phase(self.player2)
            res = research_phase(self.player3)
            #current_player = get_next_player(res["players"])
        else:
            print("phase should be 'research' but is " + str(res["game"]["phase"]))
            exit(-1)

        return res