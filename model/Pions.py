class Pions :
    def __init__(self, nom) :
        self.name = nom
        self._position = None
        print("Pions initiés !")
        
    def getPosition(self):
        return self._position
    
    def setPosition(self, position):
        self.position = _position

    position = property(getPosition, setPosition)
