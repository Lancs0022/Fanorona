from model.Joueur import Joueur  # Adjust the import path based on your project structure
import model.Pions as Pion
import numpy as np
class IA(Joueur):
    def __init__(self, nom, side, gameState):
        self.sommetFiltre = np.zeros((3,3))
        self.nom = nom
        self.side = side
        self.pions = [Pion(1*side), Pion(2*side), Pion(3*side)]
        self.gameState = gameState
        # Redéfinitions des arètes pour les pions
        self.arets = {
            (0,0): ((0,1), (1,0), (1,1)),
            (0,1): ((0,0), (0,2), (1,1)),
            (0,2): ((0,1), (1,2), (1,1)),
            (1,0): ((0,0), (1,1), (2,0)),
            (1,1): ((0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)),
            (1,2): ((0,2), (1,1), (2,2)),
            (2,0): ((1,0), (1,1), (2,1)),
            (2,1): ((2,0), (1,1), (2,2)),
            (2,2): ((1,2), (1,1), (2,1))
        }
    
    def bougerPion(self, deplacerPionCallback):
        print("IA bouge un pion 101481872")
        deplacerPionCallback((0, 0), (0, 1))
        return True
    
    def actualiserState(self, gameState):
        self.gameState = gameState
    
    def deciderDuDeplacement(self):
        if(self.gameState.tour == self.nom):
            # self.bougerPion(pass)
        # self.gameState.sommets
            pass

    def filtrerSommet(self):
        # Les pions alliés sont positifs, les pions adverses sont négatifs.
        # On utilisera Joueur.side qui est 1 ou -1 pour déterminer le côté de l'IA.
        self.sommetFiltre[self.gameState.sommets<0] = -1
        self.sommetFiltre[self.gameState.sommets>0] = 1
        print(self.sommetFiltre)
    
    def positionsDesPions(self):
        for i in range(4):
            indices = np.where(self.gameState.sommets == self.side*(i+1))
            self.pions[i].positionActuelle = list(zip(indices[0], indices[1]))
    
    def mouvementsPossibles(self):
        # Algorithme pour déterminer les mouvements possibles
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
        
        pass
    
    def verifierPions(self):
        # Algorithme pour vérifier si un pion peut bouger
        pass
    
    