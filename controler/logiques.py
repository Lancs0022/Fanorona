import random
import numpy as np
from model.Pions import Pions
from model.Plan import Plan
from model.Joueur import Joueur
from model.IA import IA  # Import IA class if needed

class Logiques:
    def __init__(self):
        self.terrainDeJeu = Plan()
        self.initialiserPlan()
        self.gameOver = False
        self.joueur1 = Joueur("Joueur1", 1)
        self.joueur2 = Joueur("Joueur2", -1)
        self.compteurJ1 = 0
        self.compteurJ2 = 0
        self.tour_count = 0
        self.setJ1vsJ2()
        self.pionsInf = [Pions(1), Pions(2), Pions(3)]
        self.pionsSup = [Pions(-1), Pions(-2), Pions(-3)]
        # self.quelMode()
        print(self.terrainDeJeu.getSommet())
        print("C'est au tour de/du : ", self.tour)
        # self.deplacerPion((2,0), (1,0))
        # self.deplacerPion((0,1), (1,1))

    def initialiserPlan(self):
        for i in range(3):
            self.terrainDeJeu.setSommet((2, i), i + 1)  # Pions inférieurs
            self.terrainDeJeu.setSommet((0, i), -i - 1)  # Pions supérieurs
            self.terrainDeJeu.setSommet((1, i), 0)  # Cases vides
        print(self.terrainDeJeu.getSommet())
        
    def mouvementEstPossible(self, posDepart, posArrivee):
        if posArrivee in self.terrainDeJeu.arets.get(posDepart, []) and self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] == 0:
            return True
        return False

    def positionsDesPions(self, listeDePions, side):
        """
        Met à jour les positions actuelles des pions pour un joueur donné.
        """
        for i, pion in enumerate(listeDePions):
            indices = np.where(self.terrainDeJeu.getSommet() == side * (i + 1))
            pion.positionActuelle = list(zip(indices[0], indices[1]))

    def mouvementsPossibles(self):
        """
            - D'abord la grille du jeu est une matrice 3x3 dont les valeurs sont 0, 1, -1, 2, -2, 3, -3
            - Ces pions peuvent se déplacer selon la carte suivante:
                (0,0): ((0,1), (1,0), (1,1)),
                (0,1): ((0,0), (0,2), (1,1)),
                (0,2): ((0,1), (1,2), (1,1)),
                (1,0): ((0,0), (1,1), (2,0)),
                (1,1): ((0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)),
                (1,2): ((0,2), (1,1), (2,2)),
                (2,0): ((1,0), (1,1), (2,1)),
                (2,1): ((2,0), (1,1), (2,2)),
                (2,2): ((1,2), (1,1), (2,1))
            - Pour commencer, on regarde la position de chaque pion dans la liste des pions
            - Ensuite, pour le sommet i on regarde le dico des arètes pour voir où il peut se déplacer
            - On vérifie si la position d'arrivée est occupée par un pion adverse
            - Si c'est non alors on ajoute la position d'arrivée à la liste des mouvements possibles pour ce pion
        """
        # Met à jour les positions des pions
        self.positionsDesPions(self.pionsInf, side=1)
        self.positionsDesPions(self.pionsSup, side=-1)
        
        self.mouvementsPossiblesInf = {
            self.pionsInf[0]: [],
            self.pionsInf[1]: [],
            self.pionsInf[2]: []
        }
        self.mouvementsPossiblesSup = {
            self.pionsSup[0]: [],
            self.pionsSup[1]: [],
            self.pionsSup[2]: []
        }

        # Parcourir les pions inférieurs
        for pion in self.pionsInf:
            for position in pion.positionActuelle:
                for voisin in self.terrainDeJeu.arets.get(position, []):
                    if self.terrainDeJeu.sommets[voisin[0], voisin[1]] >= 0:  # Case libre ou alliée
                        self.mouvementsPossiblesInf[pion].append(voisin)
        # Parcourir les pions supérieurs
        for pion in self.pionsSup:
            for position in pion.positionActuelle:
                for voisin in self.terrainDeJeu.arets.get(position, []):
                    if self.terrainDeJeu.sommets[voisin[0], voisin[1]] <= 0:  # Case libre ou alliée
                        self.mouvementsPossiblesSup[pion].append(voisin)

    def deplacerPion(self, posDepart, posArrivee):
        if self.gameOver:
            return "Partie terminée"
        
        print(f"Demande de déplacement du pion {self.terrainDeJeu.sommets[posDepart[0], posDepart[1]]} de {posDepart} à {posArrivee}")
        
        # Vérifiez si un pion est présent à la position de départ
        if self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] == 0:
            return "Pas de pion à cette position"
        
        # Appelez mouvementsPossibles pour mettre à jour les mouvements possibles
        self.mouvementsPossibles()
        
        # Vérifiez si le mouvement est autorisé
        pion = self.terrainDeJeu.sommets[posDepart[0], posDepart[1]]
        if pion > 0:  # Pion inférieur
            if posArrivee not in self.mouvementsPossiblesInf[self.pionsInf[abs(pion) - 1]]:
                return "Mouvement non autorisé"
        elif pion < 0:  # Pion supérieur
            if posArrivee not in self.mouvementsPossiblesSup[self.pionsSup[abs(pion) - 1]]:
                return "Mouvement non autorisé"
        
        # Effectuez le déplacement
        self.terrainDeJeu.sommets[posArrivee[0], posArrivee[1]] = pion
        self.terrainDeJeu.sommets[posDepart[0], posDepart[1]] = 0
        self.tour_count += 1
        
        # Changez le tour
        if self.tour == self.joueur1:
            self.compteurJ1 += 1
            self.tour = self.joueur2
        else:
            self.compteurJ2 += 1
            self.tour = self.joueur1
        
        print("Pion déplacé !")
        print(f"C'est au tour de/du : {self.tour.nom}")
        print(self.terrainDeJeu.sommets)
        return True

    def verifierLigne(self, positions):
        """
        Vérifie si une ligne donnée entraîne une victoire pour un joueur.
        
        Logique :
        - Une ligne est définie par une liste de positions (exemple : [(0, 0), (0, 1), (0, 2)]).
        - On récupère les valeurs des sommets correspondants à ces positions.
        - Si toutes les valeurs sont positives (> 0), cela signifie que la ligne est occupée par les pions du joueur 1.
        - Si toutes les valeurs sont négatives (< 0), cela signifie que la ligne est occupée par les pions du joueur 2.
        - Exception : Si le compteur de tours (`self.tour_count`) est inférieur à 10, les positions de départ ne comptent pas comme une victoire.
          - Exemple de positions de départ :
            - Joueur 1 : [[1, 2, 3], [x, x, x], [x, x, x]]
            - Joueur 2 : [[x, x, x], [x, x, x], [-1, -2, -3]]
        - Retourne :
          - `self.quiGagne(self.joueur1)` si le joueur 1 gagne.
          - `self.quiGagne(self.joueur2)` si le joueur 2 gagne.
          - `0` si aucune victoire n'est détectée.
        """
        valeurs = [self.terrainDeJeu.sommets[x, y] for x, y in positions]

        # Vérifie si toutes les valeurs sont positives (joueur 1)
        if all(v > 0 for v in valeurs):
            # Exception : Vérifie si les positions correspondent à la disposition initiale des pions du joueur 1
            if self.tour_count < 10 and sorted(valeurs) == [1, 2, 3]:
                return 0  # Pas de victoire
            return self.quiGagne(self.joueur1)

        # Vérifie si toutes les valeurs sont négatives (joueur 2)
        elif all(v < 0 for v in valeurs):
            # Exception : Vérifie si les positions correspondent à la disposition initiale des pions du joueur 2
            if self.tour_count < 10 and sorted(valeurs) == [-3, -2, -1]:
                return 0  # Pas de victoire
            return self.quiGagne(self.joueur2)

        # Pas de victoire
        return 0

    def aGagnee(self):
        lignes = [
            [(i, 0), (i, 1), (i, 2)] for i in range(3)  # Lignes horizontales
        ] + [
            [(0, i), (1, i), (2, i)] for i in range(3)  # Colonnes verticales
        ] + [
            [(0, 0), (1, 1), (2, 2)],  # Diagonale principale
            [(0, 2), (1, 1), (2, 0)]   # Diagonale secondaire
        ]
        for ligne in lignes:
            resultat = self.verifierLigne(ligne)
            if resultat:
                return resultat
        return 0
    
    def quiGagne(self, joueur):
        print("{} a gagné !".format(joueur.nom))
        self.gameOver = True
        if joueur == self.joueur1.nom:
            return 1
        elif joueur == self.joueur2.nom:
            return 2

    def setJoueur1(self, nom):
        self.joueur1.nom = nom
    def setJoueur2(self, nom):
        self.joueur2.nom = nom
    def setJ1vsJ2(self):
        self.joueur1.nom = "Joueur1"
        self.joueur2.nom = "Joueur2"
        self.tour = random.choice([self.joueur1, self.joueur2])
    def setJ1vsIA(self):
        self.joueur1.nom = "Joueur1"
        self.joueur2 = IA("IA", self.terrainDeJeu)  # Utilisez IA pour joueur2
        self.tour = random.choice([self.joueur1, self.joueur2])

    def quelMode(self):
        print("Quel mode de jeu voulez-vous ?")
        print("1. Joueur1 vs Joueur2")
        print("2. Joueur1 vs IA")
        print("3. IA vs IA")
        mode = input("Entrez le numéro du mode de jeu : ")
        if mode == "1":
            self.setJ1vsJ2()
        elif mode == "2":
            self.setJ1vsIA()
        elif mode == "3":
            self.setIAvsIA()
        else:
            print("Mode de jeu invalide")
            self.quelMode()
