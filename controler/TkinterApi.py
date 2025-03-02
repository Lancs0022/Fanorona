from functools import partial
from vue.TkinterVue import TkinterVue as tkVue
from controler.logiques import Logiques

class TkinterApi(Logiques):
    def __init__(self):
        super().__init__()
        self.selected_pion = None
        self.vue = tkVue(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, partial(self.on_click), self.nouveauJeu)
        self.vue.dessinerTerrain()
        self.vue.lierEvenementClic(partial(self.on_click))
        self.vue.run()

    def on_click(self, event):
        print(f"on_click called with event: {event}")
        print(f"self is instance of TkinterApi: {isinstance(self, TkinterApi)}")
        print(f"self.vue is instance of TkinterVue: {isinstance(self.vue, tkVue)}")
        x, y = event.x, event.y
        for (i, j), (sx, sy) in self.vue.sommet_positions.items():
            if (sx - 10 <= x <= sx + 10) and (sy - 10 <= y <= sy + 10):
                if self.selected_pion:
                    if self.deplacerPion(self.selected_pion, (i, j)):
                        self.vue.dessinerTerrain()
                    self.selected_pion = None
                elif self.terrainDeJeu.sommets[i, j] != 0:
                    self.selected_pion = (i, j)
                break

    def aGagnee(self):
        # Victoire par position horizontale
        for i in range(3):
            if self.terrainDeJeu.sommets[i, 0] > 0 and self.terrainDeJeu.sommets[i, 1] > 0 and self.terrainDeJeu.sommets[i, 2] > 0:
                if not (self.terrainDeJeu.sommets[2, 0] == 1 and self.terrainDeJeu.sommets[2, 1] == 2 and self.terrainDeJeu.sommets[2, 2] == 3) or self.tour_count > 10:
                    self.vue.victoire(self.joueur1)
                    return True
            elif self.terrainDeJeu.sommets[i, 0] < 0 and self.terrainDeJeu.sommets[i, 1] < 0 and self.terrainDeJeu.sommets[i, 2] < 0:
                if not (self.terrainDeJeu.sommets[0, 0] == -1 and self.terrainDeJeu.sommets[0, 1] == -2 and self.terrainDeJeu.sommets[0, 2] == -3) or self.tour_count > 10:
                    self.vue.victoire(self.joueur2)
                    return True

        # Victoire par position verticale
        for i in range(3):
            if self.terrainDeJeu.sommets[0, i] > 0 and self.terrainDeJeu.sommets[1, i] > 0 and self.terrainDeJeu.sommets[2, i] > 0:
                self.vue.victoire(self.joueur1)
                return True
            elif self.terrainDeJeu.sommets[0, i] < 0 and self.terrainDeJeu.sommets[1, i] < 0 and self.terrainDeJeu.sommets[2, i] < 0:
                self.vue.victoire(self.joueur2)
                return True

        # Victoire par position diagonale
        if self.terrainDeJeu.sommets[0, 0] > 0 and self.terrainDeJeu.sommets[1, 1] > 0 and self.terrainDeJeu.sommets[2, 2] > 0:
            self.vue.victoire(self.joueur1)
            return True
        elif self.terrainDeJeu.sommets[0, 0] < 0 and self.terrainDeJeu.sommets[1, 1] < 0 and self.terrainDeJeu.sommets[2, 2] < 0:
            self.vue.victoire(self.joueur2)
            return True
        elif self.terrainDeJeu.sommets[0, 2] > 0 and self.terrainDeJeu.sommets[1, 1] > 0 and self.terrainDeJeu.sommets[2, 0] > 0:
            self.vue.victoire(self.joueur1)
            return True
        elif self.terrainDeJeu.sommets[0, 2] < 0 and self.terrainDeJeu.sommets[1, 1] < 0 and self.terrainDeJeu.sommets[2, 0] < 0:
            self.vue.victoire(self.joueur2)
            return True

        return False

    def nouveauJeu(self):
        self.initialiserPlan()
        self.gameOver = False
        self.vue.connecterLesDonnees(self.terrainDeJeu.sommets, self.terrainDeJeu.arets)
        self.vue.dessinerTerrain()
    # ...existing code...