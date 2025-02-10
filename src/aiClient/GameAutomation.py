from AiPlayer import create_game, Player, initial_research_phase, turn, draft, research_phase
from ClientGame import ClientGame
import http.client
from multiprocessing import Process

THREADS_COUNT = 1

player1 = None
player2 = None
player3 = None

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
    #print("Generation " + str(res["game"]["generation"]))
    current_player = get_next_player(res["players"])

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
            print("run id: " + old_res["game"]["runId"])
            print("player id: " + old_res["game"]["id"])
            print("Players not in res:")
            print("old res:")
            print(old_res)
            print(res)
            exit(-1)

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
        res = draft(player3)
    elif res["game"]["phase"] == "end":
        #print("The game has ended ", end="")
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
        research_phase(player1)
        research_phase(player2)
        res = research_phase(player3)
        #current_player = get_next_player(res["players"])
    else:
        print("phase should be 'research' but is " + str(res["game"]["phase"]))
        exit(-1)

    return res

#while True:
#    res = generation(res)

def game():
    new_game = create_game()
    #print("New game created")

    global player1, player2, player3
    player1 = Player(new_game["players"][0]["color"], new_game["players"][0]["id"], new_game["players"][0]["name"])
    player2 = Player(new_game["players"][1]["color"], new_game["players"][1]["id"], new_game["players"][1]["name"])
    player3 = Player(new_game["players"][2]["color"], new_game["players"][2]["id"], new_game["players"][2]["name"])

    initial_research_phase(player1)
    initial_research_phase(player2)
    res = initial_research_phase(player3)

    while True:
        res = generation(res)
        if res is None:
            break



import time

times = []

while False:
    start_time = time.time()
    game()
    duration = time.time() - start_time
    times.append(duration)
    average = sum(times) / len(times)
    print("average game time: " + str(average) + ", last: " + str(times[-1]))


start_time = time.time()
games_count = 0

def loop(http_connection, name):
    http_connection = http.client.HTTPConnection("localhost", 8080)
    while True:
        start_time1 = time.time()
        client_game1 = ClientGame(http_connection)
        client_game1.start()
        duration1 = time.time() - start_time1
        times.append(duration1)
        average = sum(times) / len(times)
        #print("average game time in (" + name + "): " + str(average) + ", last: " + str(times[-1]))
        current_time = time.time()
        print(name + ": " + str((current_time-start_time)/len(times)) + "(" + str(current_time-start_time) + ", " + str(len(times)) + ")")
        #break

import threading

if __name__ == '__main__':
    for i in range(THREADS_COUNT):
        http_connectionx = http.client.HTTPConnection("localhost", 8080)
        thread = threading.Thread(target=loop, args=(http_connectionx, "thread" + str(i)))
        thread.start()
        time.sleep(0.75)