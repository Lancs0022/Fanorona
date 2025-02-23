class Pions :
    def __init__(self, nom) :
        self._name = nom
        print("Pions initiés !")
        
    def getName(self):
        return self._name
    
    def setName(self, name):
        self.name = name
        
    property(getName, setName)
