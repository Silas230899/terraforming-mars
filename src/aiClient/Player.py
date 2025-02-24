class Player:
    game_age = 0
    undo_count = 0
    run_id = ""

    def __init__(self, color, id, name):
        self.color = color
        self.id = id
        self.name = name
