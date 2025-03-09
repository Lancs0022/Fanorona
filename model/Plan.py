import numpy as np

class Plan:
    def __init__(self):
        self._sommets = np.zeros((3,3), dtype=int)
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
        print("Plan initiés !")

    def setSommet(self, position, valeur):
        self._sommets[position[0], position[1]] = valeur
        
    def copieSommets(self, copieSommets):
        self._sommets = copieSommets
    
    def getSommet(self):
        return self._sommets
    
    sommets = property(getSommet, setSommet)
