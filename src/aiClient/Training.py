from AiPlayer import create_game, Player, initial_research_phase, turn, draft, research_phase

new_game = create_game()
print("New game created")

player1 = Player(new_game["players"][0]["color"], new_game["players"][0]["id"], new_game["players"][0]["name"])
player2 = Player(new_game["players"][1]["color"], new_game["players"][1]["id"], new_game["players"][1]["name"])
player3 = Player(new_game["players"][2]["color"], new_game["players"][2]["id"], new_game["players"][2]["name"])

initial_research_phase(player1)
initial_research_phase(player2)
res = initial_research_phase(player3)

# wenn man normal dran ist ist man active und die anderen nicht, im draft wenn quasi alle dran sind ist man selbst nicht active
def get_next_player(players):
    for player in players:
        if player["isActive"]:
            if player1.name == player["name"]:
                return player1
            elif player2.name == player["name"]:
                return player2
            elif player3.name == player["name"]:
                return player3

def generation(res):
    print("Generation " + str(res["game"]["generation"]))
    current_player = get_next_player(res["players"])

    while res["game"]["phase"] == "action":
        if "waitingFor" in res:
            print("waiting for something")
        else:
            print("not waiting for something")

        res = turn(current_player)
        current_player = get_next_player(res["players"])

    if res["game"]["phase"] == "drafting":
        draft(player1)
        draft(player2)
        draft(player3)

        draft(player1)
        draft(player2)
        draft(player3)

        draft(player1)
        draft(player2)
        draft(player3)

    if res["game"]["phase"] == "research":
        research_phase(player1)
        research_phase(player2)
        res = research_phase(player3)
        #current_player = get_next_player(res["players"])
    return res


res = generation(res)
generation(res)



