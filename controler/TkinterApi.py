from functools import partial
from vue.TkinterVue import TkinterVue as tkVue
from controler.logiques import Logiques
from controler.Tracer import Tracer
import ast
import numpy as np

class TkinterApi(Logiques):
    def __init__(self):
        super().__init__()
        self.selected_pion = None
        self.tracer = Tracer()
        self.vue = tkVue(partial(self.on_click))
        self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, self.joueur1, self.joueur2)
        self.vue.actualiserTour(self.tour)
        self.vue.chargerMenu(self.nouveauJeu, self.sauvegarderLaPartie, self.chargerPartie)
        self.vue.dessinerTerrain()
        self.vue.lierEvenementClic(partial(self.on_click))
        self.vue.run()

    def on_click(self, event):
        x, y = event.x, event.y
        for (i, j), (sx, sy) in self.vue.sommet_positions.items():
            if (sx - 10 <= x <= sx + 10) and (sy - 10 <= y <= sy + 10):
                if self.selected_pion:
                    result = self.deplacerPion(self.selected_pion, (i, j))
                    self.tracer.log_move(self.tour, self.selected_pion, (i, j))
                    self.selected_pion = None
                    self.vue.selectionnerPion(None, None)
                    if result is True:
                        self.vue.actualiserTour(self.tour)
                    else:
                        self.vue.afficherErreur(result)
                    self.vue.dessinerTerrain()
                    self.aGagnee()
                elif self.terrainDeJeu.sommets[i, j] != 0:
                    print(f"Sélection du pion en {self.terrainDeJeu.sommets[i, j]} en ({i}, {j})")
                    self.selected_pion = (i, j)
                    self.vue.selectionnerPion(i, j)
                    self.vue.dessinerTerrain()
                break

    def aGagnee(self):
        # Victoire par position horizontale
        for i in range(3):
            if self.terrainDeJeu.sommets[i, 0] > 0 and self.terrainDeJeu.sommets[i, 1] > 0 and self.terrainDeJeu.sommets[i, 2] > 0:
                if not (self.terrainDeJeu.sommets[2, 0] == 1 and self.terrainDeJeu.sommets[2, 1] == 2 and self.terrainDeJeu.sommets[2, 2] == 3) or self.tour_count > 10:
                    self.vue.victoire(self.joueur1)
                    return self.quiGagne(self.joueur1)
            elif self.terrainDeJeu.sommets[i, 0] < 0 and self.terrainDeJeu.sommets[i, 1] < 0 and self.terrainDeJeu.sommets[i, 2] < 0:
                if not (self.terrainDeJeu.sommets[0, 0] == -1 and self.terrainDeJeu.sommets[0, 1] == -2 and self.terrainDeJeu.sommets[0, 2] == -3) or self.tour_count > 10:
                    self.vue.victoire(self.joueur2)
                    return self.quiGagne(self.joueur2)

        # Victoire par position verticale
        for i in range(3):
            if self.terrainDeJeu.sommets[0, i] > 0 and self.terrainDeJeu.sommets[1, i] > 0 and self.terrainDeJeu.sommets[2, i] > 0:
                self.vue.victoire(self.joueur1)
                return self.quiGagne(self.joueur1)
            elif self.terrainDeJeu.sommets[0, i] < 0 and self.terrainDeJeu.sommets[1, i] < 0 and self.terrainDeJeu.sommets[2, i] < 0:
                self.vue.victoire(self.joueur2)
                return self.quiGagne(self.joueur2)

        # Victoire par position diagonale
        if self.terrainDeJeu.sommets[0, 0] > 0 and self.terrainDeJeu.sommets[1, 1] > 0 and self.terrainDeJeu.sommets[2, 2] > 0:
            self.vue.victoire(self.joueur1)
            self.tracer.log_victory(self.joueur1)
            return self.quiGagne(self.joueur1)
        elif self.terrainDeJeu.sommets[0, 0] < 0 and self.terrainDeJeu.sommets[1, 1] < 0 and self.terrainDeJeu.sommets[2, 2] < 0:
            self.vue.victoire(self.joueur2)
            self.tracer.log_victory(self.joueur2)
            return self.quiGagne(self.joueur2)
        elif self.terrainDeJeu.sommets[0, 2] > 0 and self.terrainDeJeu.sommets[1, 1] > 0 and self.terrainDeJeu.sommets[2, 0] > 0:
            self.vue.victoire(self.joueur1)
            return self.quiGagne(self.joueur1)
        elif self.terrainDeJeu.sommets[0, 2] < 0 and self.terrainDeJeu.sommets[1, 1] < 0 and self.terrainDeJeu.sommets[2, 0] < 0:
            self.vue.victoire(self.joueur2)
            return self.quiGagne(self.joueur2)

        return 0

    def nouveauJeu(self):
        self.tour_count = 0
        self.compteurJ1 = 0
        self.compteurJ2 = 0
        self.initialiserPlan()
        self.gameOver = False
        self.tracer.log("Nouveau jeu")
        self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, self.joueur1, self.joueur2)
        self.vue.dessinerTerrain()
        
    def sauvegarderLaPartie(self):
        if self.gameOver:
            self.vue.afficherErreur("Partie terminée, impossible de sauvegarder.")
            return
        game_state = [
            f"Tour: {self.tour}",
            f"Joueur1: {self.joueur1}",
            f"Joueur2: {self.joueur2}",
            f"Sommets: {self.terrainDeJeu.sommets.tolist()}"
        ]
        self.tracer.save_game(game_state)

    def chargerPartie(self):
        try:
            self.gameOver = False
            print("Avant le chargement de la partie...")
            print("Sommets: ", self.terrainDeJeu.sommets)
            print("Le type de sommets: ", type(self.terrainDeJeu.sommets))
            print("Tour: ", self.tour)
            print("Joueur1: ", self.joueur1)
            print("Joueur2: ", self.joueur2)
            print("Tour count: ", self.tour_count)
            print("Compteur J1: ", self.compteurJ1)
            print("Compteur J2: ", self.compteurJ2)
            print("Chargement de la partie...")
            with open(self.tracer.save_filename, 'r') as file:
                lines = file.readlines()
            
            if len(lines) < 4:
                raise ValueError("Fichier de sauvegarde corrompu ou incomplet.")
            
            self.tour = lines[0].strip().split(": ")[1]
            self.joueur1 = lines[1].strip().split(": ")[1]
            self.joueur2 = lines[2].strip().split(": ")[1]
            
            # Combine all lines after "Sommets: " into a single string
            sommets_str = "".join(lines[3:6]).strip().split(": ", 1)[1]
            self.terrainDeJeu.copieSommets(np.array(ast.literal_eval(sommets_str)))
            print("Les données ont été chargées avec succès !")
            print("Sommets: ", self.terrainDeJeu.sommets)
            print("Le type de sommets: ", type(self.terrainDeJeu.sommets))
            print("Tour: ", self.tour)
            print("Joueur1: ", self.joueur1)
            print("Joueur2: ", self.joueur2)
            print("Tour count: ", self.tour_count)
            print("Compteur J1: ", self.compteurJ1)
            print("Compteur J2: ", self.compteurJ2)
            # Code commenté
            # self.terrainDeJeu.arets = ast.literal_eval(lines[6].strip().split(": ", 1)[1])
            # self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, self.joueur1, self.joueur2)
            
            self.vue.actualiserTour(self.tour)
            self.vue.actualiserSommets(self.terrainDeJeu.sommets)
        
        except (FileNotFoundError, ValueError, SyntaxError) as e:
            self.vue.afficherErreur(f"Erreur de chargement: {str(e)}")
        
    def actualiserInformations(self):
        self.vue.actualiserInformations(self.joueur1, self.joueur2, self.tour_count)