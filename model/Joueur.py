class Joueur:
    def __init__(self, nom, side):
        self.nom = nom
        self.side = side

    def __str__(self):
        return f"{self.nom} {self.side}"