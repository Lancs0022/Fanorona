import tkinter as tk
from tkinter import messagebox

class TkinterVue:
    def __init__(self, sommets, aretes, on_click_callback, nouveau_jeu_callback):
        self.fenPrincipal = tk.Tk()
        self.fenPrincipal.title("Fanorona :)")
        self.fenPrincipal.geometry("600x400")
        self.fenPrincipal.minsize(480, 240)

        self.chargerMenu(nouveau_jeu_callback)
        self.connecterLesDonnees(sommets, aretes)
        self.creerFrames()
        self.fenPrincipal.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", on_click_callback)

    def chargerMenu(self, nouveau_jeu_callback):
        # Crée la barre de menu
        self.menuBar = tk.Menu(self.fenPrincipal)
        
        # Crée le menu "Fichier"
        self.menuFichier = tk.Menu(self.menuBar, tearoff=0)
        self.menuFichier.add_command(label="Nouveau", command=nouveau_jeu_callback)
        self.menuFichier.add_command(label="Ouvrir")
        self.menuFichier.add_command(label="Enregistrer")
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label="Quitter", command=self.fenPrincipal.quit)
        
        # Crée le menu "Édition"
        self.menuEdition = tk.Menu(self.menuBar, tearoff=0)
        self.menuEdition.add_command(label="Annuler")
        self.menuEdition.add_command(label="Refaire")
        
        # Crée le menu "Aide"
        self.menuAide = tk.Menu(self.menuBar, tearoff=0)
        self.menuAide.add_command(label="À propos")
        
        # Ajoute les menus à la barre de menu
        self.menuBar.add_cascade(label="Fichier", menu=self.menuFichier)
        self.menuBar.add_cascade(label="Édition", menu=self.menuEdition)
        self.menuBar.add_cascade(label="Aide", menu=self.menuAide)
        
        # Configure la fenêtre principale pour afficher la barre de menu
        self.fenPrincipal.config(menu=self.menuBar)

    def creerFrames(self):
        # Crée le frame du haut
        self.frameHaut = tk.Frame(self.fenPrincipal, height=0.7*40)
        self.frameHaut.pack(fill=tk.X)
        
        # Crée le frame du milieu
        self.frameMilieu = tk.Frame(self.fenPrincipal, height=0.7*80)
        self.frameMilieu.pack(fill=tk.BOTH, expand=True)
        
        # Crée le frame du bas
        self.frameBas = tk.Frame(self.fenPrincipal, height=0.7*40)
        self.frameBas.pack(fill=tk.X)
        
        # Ajoute des labels aux frames
        self.labelHaut = tk.Label(self.frameHaut, text="Informations du jeu")
        self.labelHaut.pack()
        
        self.labelBas = tk.Label(self.frameBas, text="Statut du jeu")
        self.labelBas.pack()

        # Create a canvas in the middle frame
        self.canvas = tk.Canvas(self.frameMilieu)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    # Méthode pour dessiner un cercle
    def drawCircle(self, x, y, r=5, color="black"):
        # Draw a circle on the canvas
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)

    # Méthode pour dessiner une ligne
    def drawLine(self, x1, y1, x2, y2, color="black"):
        # Draw a line on the canvas
        self.canvas.create_line(x1, y1, x2, y2, fill=color)

    # Méthode pour dessiner les sommets
    def dessinerSommets(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        padding = 20
        cell_width = (width - 2 * padding) / 2
        cell_height = (height - 2 * padding) / 2

        self.sommet_positions = {}
        for i in range(3):
            for j in range(3):
                x = padding + j * cell_width
                y = padding + i * cell_height
                self.sommet_positions[(i, j)] = (x, y)
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")

    # Méthode pour dessiner les arêtes
    def dessinerAretes(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        padding = 20
        cell_width = (width - 2 * padding) / 2
        cell_height = (height - 2 * padding) / 2

        for (x1, y1), voisins in self.aretes.items():
            x1 = padding + x1 * cell_width
            y1 = padding + y1 * cell_height
            for (x2, y2) in voisins:
                x2 = padding + x2 * cell_width
                y2 = padding + y2 * cell_height
                self.canvas.create_line(x1, y1, x2, y2, fill="black")

    # Méthode pour dessiner les pions
    def dessinerPions(self):
        for (i, j), (x, y) in self.sommet_positions.items():
            pion = self.sommets[i, j]
            if pion > 0:
                color = "blue"
                r = 10
            elif pion < 0:
                color = "red"
                r = 10
            else:
                continue
            self.drawCircle(x, y, r, color)

    # Méthode pour dessiner le terrain
    def dessinerTerrain(self):
        self.canvas.delete("all")
        self.dessinerAretes()
        self.dessinerSommets()
        self.dessinerPions()
        print("Terrain dessiné !")

    # Méthode pour connecter les données
    def connecterLesDonnees(self, sommets, aretes):
        # Connect the data to the view
        self.sommets = sommets
        self.aretes = aretes

    # Méthode pour redimensionner le canvas à chaque modification d'état de la fenêtre
    def on_resize(self, event):
        self.dessinerTerrain()

    # Méthode pour exécuter la boucle principale de Tkinter
    def run(self):
        # Run the Tkinter # Méthode pour lier l'événement de clic de souris
        self.fenPrincipal.mainloop()

    # Méthode pour lier l'événement de clic de souris
    def lierEvenementClic(self, on_click_callback):
        self.canvas.bind("<Button-1>", on_click_callback)

    def victoire(self, joueur):
        messagebox.showinfo("Victoire", f"{joueur} a gagné !")