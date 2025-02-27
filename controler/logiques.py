import random
from model.Pions import Pions
from model.Plan import Plan

class Logiques:
    def __init__(self):
        self.initialiserPlan()
        self.tour = random.choice(["Joueur", "IA"])
        print(self.terrainDeJeu.sommets)
        print("C'est au tour de/du : ", self.tour)
        self.deplacerPion((2,0), (1,0))
        self.deplacerPion((0,1), (1,1))

    def initialiserPlan(self):
        self.pionsAllies = [Pions(1), Pions(2), Pions(3)]
        self.pionsAdverse = [Pions(-1), Pions(-2), Pions(-3)]
        
        self.terrainDeJeu = Plan()
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((0,i), self.pionsAllies[i].getName())
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((2,i), self.pionsAdverse[i].getName())

    def mouvementEstPossible(self, posDepart, posArrivee):
        if posArrivee in self.terrainDeJeu.arets.get(posDepart, []) and self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] == 0:
            return True
        return False

    def deplacerPion(self, posDepart, posArrivee):
        print("Demande de déplacement du pion ", self.terrainDeJeu.sommets[posDepart[0], posDepart[1]], " de ", posDepart, " à ", posArrivee)
        
        if self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] == 0:
            print("Pas de pion à cette position")
            return False
        elif self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] != 0:
            print("Position d'arrivée déjà occupée")
            return False
        elif not self.mouvementEstPossible(posDepart, posArrivee):
            print("Mouvement non autorisé")
            return False
        else:
            if self.tour == "Joueur" and self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] > 0 or self.tour == "IA" and self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] < 0:
                self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] = self.terrainDeJeu.sommets[posDepart[0], posDepart[1]]
                self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] = 0
                self.tour = "IA" if self.tour == "Joueur" else "Joueur"
                print("Pion déplacé !")
                if self.aGagnee():
                    return "Victoire"
                print("C'est au tour de/du : ", self.tour)
                print(self.terrainDeJeu.sommets)
                return True
            else:
                print("Ce n'est pas votre tour")
                return False

    def aGagnee(self):
        # Victoire par position horizontale
        for i in range (3):
            if self.terrainDeJeu.sommets[i,0] > 0 and self.terrainDeJeu.sommets[i,1] > 0 and self.terrainDeJeu.sommets[i,2] > 0:
                print("Le joueur a gagné !")
                return True
            elif self.terrainDeJeu.sommets[i,0] < 0 and self.terrainDeJeu.sommets[i,1] < 0 and self.terrainDeJeu.sommets[i,2] < 0:
                print("L'IA a gagné !")
                return True

        # Victoire par position verticale
        for i in range (3):
            if self.terrainDeJeu.sommets[0,i] > 0 and self.terrainDeJeu.sommets[1,i] > 0 and self.terrainDeJeu.sommets[2,i] > 0:
                print("Le joueur a gagné !")
                return True
            elif self.terrainDeJeu.sommets[0,i] < 0 and self.terrainDeJeu.sommets[1,i] < 0 and self.terrainDeJeu.sommets[2,i] < 0:
                print("L'IA a gagné !")
                return True

        # Victoire par position diagonale
        if self.terrainDeJeu.sommets[0,0] > 0 and self.terrainDeJeu.sommets[1,1] > 0 and self.terrainDeJeu.sommets[2,2] > 0:
            print("Le joueur a gagné !")
            return True
        elif self.terrainDeJeu.sommets[0,0] < 0 and self.terrainDeJeu.sommets[1,1] < 0 and self.terrainDeJeu.sommets[2,2] < 0:
            print("L'IA a gagné !")
            return True
        elif self.terrainDeJeu.sommets[0,2] > 0 and self.terrainDeJeu.sommets[1,1] > 0 and self.terrainDeJeu.sommets[2,0] > 0:
            print("Le joueur a gagné !")
            return True
        elif self.terrainDeJeu.sommets[0,2] < 0 and self.terrainDeJeu.sommets[1,1] < 0 and self.terrainDeJeu.sommets[2,0] < 0:
            print("L'IA a gagné !")
            return True

        return False