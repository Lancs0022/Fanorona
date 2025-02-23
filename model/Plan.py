import numpy as np

class Plan :
    # grille = np.array(zeros(3,3))
    def __init__(self) :
        self._sommets = np.zeros((3,3))
        self.arets = {
            1: (1, 2, 4 ,5),
            2: (2, 1, 3, 5),
            3: (3, 2, 6, 5),
            4: (4, 1, 7, 5),
            5: (5, 1, 2, 3, 4, 6, 7, 8, 9),
            6: (6, 3, 9, 5),
            7: (7, 4, 8, 5),
            8: (8, 7, 9, 5),
            9: (9, 6, 8, 5)
        }
        print("Plan initiés !")

    def setSommet(self, position, valeur):
        self._sommets[position[0], position[1]] = valeur
    
    def getSommet(self):
        return self._sommets
    
    sommets = property(getSommet, setSommet)
