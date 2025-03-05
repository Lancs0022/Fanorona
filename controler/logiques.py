import random
from model.Pions import Pions
from model.Plan import Plan

class Logiques:
    def __init__(self):
        self.initialiserPlan()
        self.gameOver = False
        self.joueur1 = "Joueur1"
        self.joueur2 = "Joueur2"
        self.compteurJ1 = 0
        self.compteurJ2 = 0
        self.tour_count = 0
        self.setJ1vsJ2()
        print(self.terrainDeJeu.sommets)
        print("C'est au tour de/du : ", self.tour)
        # Retirer les appels à deplacerPion pour éviter d'appeler aGagnee avant que self.vue soit initialisé
        # self.deplacerPion((2,0), (1,0))
        # self.deplacerPion((0,1), (1,1))

    def initialiserPlan(self):
        self.pionsAllies = [Pions(1), Pions(2), Pions(3)]
        self.pionsAdverse = [Pions(-1), Pions(-2), Pions(-3)]
        
        self.terrainDeJeu = Plan()
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((2,i), self.pionsAllies[i].getName())
        for i in range(3):
            print(i)
            self.terrainDeJeu.setSommet((0,i), self.pionsAdverse[i].getName())
            
    def setJoueur1(self, nom):
        self.joueur1 = nom
    def setJoueur2(self, nom):
        self.joueur2 = nom
    def setJ1vsJ2(self):
        self.joueur1 = "Joueur1"
        self.joueur2 = "Joueur2"
        self.tour = random.choice([self.joueur1, self.joueur2])
    def setJ1vsIA(self):
        self.joueur1 = "Joueur1"
        self.joueur2 = "IA"
        self.tour = random.choice([self.joueur1, self.joueur2])

    def mouvementEstPossible(self, posDepart, posArrivee):
        if posArrivee in self.terrainDeJeu.arets.get(posDepart, []) and self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] == 0:
            return True
        return False

    def deplacerPion(self, posDepart, posArrivee):
        if self.gameOver:
            return "Partie terminée"
        print("Demande de déplacement du pion ", self.terrainDeJeu.sommets[posDepart[0], posDepart[1]], " de ", posDepart, " à ", posArrivee)
        
        if self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] == 0:
            return "Pas de pion à cette position"
        elif self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] != 0:
            return "Position d'arrivée déjà occupée"
        elif not self.mouvementEstPossible(posDepart, posArrivee):
            return "Mouvement non autorisé"
        else:
            if self.tour == "Joueur1" and self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] > 0 or ((self.tour == "IA" or self.tour == "Joueur2") and self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] < 0):
                self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] = self.terrainDeJeu.sommets[posDepart[0], posDepart[1]]
                self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] = 0
                self.tour_count += 1
                if self.tour == "Joueur1":
                    self.compteurJ1 += 1
                    self.tour = self.joueur2
                elif self.tour == "Joueur2" or self.tour == "IA":
                    self.compteurJ2 += 1
                    self.tour = self.joueur1
                print("Pion déplacé !")
                # self.aGagnee()
                print("C'est au tour de/du : ", self.tour)
                print(self.terrainDeJeu.sommets)
                return True
            else:
                return "Ce n'est pas votre tour"

    def aGagnee(self):
        # Victoire par position horizontale
        for i in range (3):
            if self.terrainDeJeu.sommets[i,0] > 0 and self.terrainDeJeu.sommets[i,1] > 0 and self.terrainDeJeu.sommets[i,2] > 0:
                if not (self.terrainDeJeu.sommets[2,0] == 1 and self.terrainDeJeu.sommets[2,1] == 2 and self.terrainDeJeu.sommets[2,2] == 3) or self.tour_count > 10:
                    return self.quiGagne(self.joueur1)
            elif self.terrainDeJeu.sommets[i,0] < 0 and self.terrainDeJeu.sommets[i,1] < 0 and self.terrainDeJeu.sommets[i,2] < 0:
                if not (self.terrainDeJeu.sommets[0,0] == -1 and self.terrainDeJeu.sommets[0,1] == -2 and self.terrainDeJeu.sommets[0,2] == -3) or self.tour_count > 10:
                    return self.quiGagne(self.joueur2)

        # Victoire par position verticale
        for i in range (3):
            if self.terrainDeJeu.sommets[0,i] > 0 and self.terrainDeJeu.sommets[1,i] > 0 and self.terrainDeJeu.sommets[2,i] > 0:
                return self.quiGagne(self.joueur1)
            elif self.terrainDeJeu.sommets[0,i] < 0 and self.terrainDeJeu.sommets[1,i] < 0 and self.terrainDeJeu.sommets[2,i] < 0:
                return self.quiGagne(self.joueur2)

        # Victoire par position diagonale
        if self.terrainDeJeu.sommets[0,0] > 0 and self.terrainDeJeu.sommets[1,1] > 0 and self.terrainDeJeu.sommets[2,2] > 0:
            return self.quiGagne(self.joueur1)
        elif self.terrainDeJeu.sommets[0,0] < 0 and self.terrainDeJeu.sommets[1,1] < 0 and self.terrainDeJeu.sommets[2,2] < 0:
            return self.quiGagne(self.joueur2)
        elif self.terrainDeJeu.sommets[0,2] > 0 and self.terrainDeJeu.sommets[1,1] > 0 and self.terrainDeJeu.sommets[2,0] > 0:
            return self.quiGagne(self.joueur1)
        elif self.terrainDeJeu.sommets[0,2] < 0 and self.terrainDeJeu.sommets[1,1] < 0 and self.terrainDeJeu.sommets[2,0] < 0:
            return self.quiGagne(self.joueur2)

        return 0
    
    def quiGagne(self, joueur):
        print("{} a gagné !".format(joueur))
        self.gameOver = True
        if joueur == "Joueur1":
            return 1
        elif joueur == "Joueur2" or joueur == "IA":
            return 2