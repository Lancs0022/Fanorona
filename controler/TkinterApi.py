from functools import partial
from vue.TkinterVue import TkinterVue as tkVue
from controler.logiques import Logiques
from controler.Tracer import Tracer

class TkinterApi(Logiques):
    def __init__(self):
        super().__init__()
        self.selected_pion = None
        self.tracer = Tracer()
        self.vue = tkVue(partial(self.on_click))
        self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, self.joueur1, self.joueur2)
        self.vue.actualiserTour(self.tour)
        self.vue.chargerMenu(self.nouveauJeu)
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
        self.initialiserPlan()
        self.gameOver = False
        self.tracer.log("Nouveau jeu")
        self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, self.joueur1, self.joueur2)
        self.vue.dessinerTerrain()
        
    def actualiserInformations(self):
        self.vue.actualiserInformations(self.joueur1, self.joueur2, self.tour_count)