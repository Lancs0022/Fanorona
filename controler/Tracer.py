import os

class Tracer:
    def __init__(self):
        self.log_filename = "log/game_log.txt"
        self.save_filename = "sauvegardes/partie.sav"
        self.create_log_file()
        self.create_save_file()

    def create_log_file(self):
        os.makedirs(os.path.dirname(self.log_filename), exist_ok=True)
        with open(self.log_filename, 'w') as file:
            file.write("Début du jeu\n")

    def create_save_file(self):
        os.makedirs(os.path.dirname(self.save_filename), exist_ok=True)
        if not os.path.exists(self.save_filename):
            with open(self.save_filename, 'w') as file:
                file.write("")

    def log(self, messages):
        with open(self.log_filename, 'a') as file:
            for message in messages:
                file.write(message + "\n")

    def log_move(self, player, from_pos, to_pos):
        message = f"{player} déplace de {from_pos} à {to_pos}"
        self.log([message])

    def log_victory(self, player):
        message = f"{player} a gagné !"
        self.log([message])

    def save_game(self, game_state):
        with open(self.save_filename, 'w') as file:
            for state in game_state:
                file.write(state + "\n")
