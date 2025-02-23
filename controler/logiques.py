from model.Pions import Pions
from model.Plan import Plan

# pion = Pions("p1")
# plan = Plan()
# plan.setSommet((0,0), 1)
# print(plan.sommets)
# print("Logique chargée !")

class Logiques:
    def __init__(self):
        self.initialiserPlan()
        print(self.terrainDeJeu.sommets)

    def initialiserPlan(self):
        self.pionsAllies = [Pions(1), Pions(2), Pions(3)]
        # self.pion1 = Pions(1)
        # self.pion2 = Pions(2)
        # self.pion3 = Pions(3)

        self.pionsAdverse = [Pions(-1), Pions(-2), Pions(-3)]
        # self.pawn1 = Pions(-1)
        # self.pawn2 = Pions(-2)
        # self.pawn3 = Pions(-3)
        
        self.terrainDeJeu = Plan()
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((0,i), self.pionsAllies[i].getName())
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((2,i), self.pionsAdverse[i].getName())
