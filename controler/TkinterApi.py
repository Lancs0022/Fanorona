import threading
from functools import partial
from vue.tkinterVue import TkinterVue as tkinterVue
from controler.logiques import Logiques

class TkinterApi(Logiques):
    def __init__(self):
        super().__init__()
        self.selected_pion = None
        self.vue = tkinterVue(self.terrainDeJeu.sommets, self.terrainDeJeu.arets, partial(self.on_click))
        self.vue.dessinerTerrain()

    def on_click(self, event):
        print(f"on_click called with event: {event}")
        print(f"self is instance of TkinterApi: {isinstance(self, TkinterApi)}")
        print(f"self.vue is instance of TkinterVue: {isinstance(self.vue, tkinterVue)}")
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
    # ...existing code...