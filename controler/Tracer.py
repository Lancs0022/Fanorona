class Tracer:
    def __init__(self, filename="game_log.txt"):
        self.filename = filename
        with open("log/" + self.filename, 'w') as file:
            file.write("Début du jeu\n")

    def log(self, message):
        with open(self.filename, 'a') as file:
            file.write(message + "\n")

    def log_move(self, player, from_pos, to_pos):
        message = f"{player} déplace de {from_pos} à {to_pos}"
        self.log(message)

    def log_victory(self, player):
        message = f"{player} a gagné !"
        self.log(message)
