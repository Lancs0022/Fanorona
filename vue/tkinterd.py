import tkinter as tk

class TkinterVue2:
    def __init__(self):
        self.fenPrincipal = tk.Tk()
        self.fenPrincipal.title("Fanorona :)")
        self.fenPrincipal.geometry("600x400")
        self.fenPrincipal.minsize(480, 240)
        
        self.label = tk.Label(self.fenPrincipal, text="Hello World")
        self.label.pack()
        self.label["text"] = "Bonjour tout le monde !"
        
        self.champ = tk.Entry(self.fenPrincipal)
        self.champ.pack()
        
        self.bouton = tk.Button(self.fenPrincipal, text="Cliquez ici")
        self.bouton.pack()
        
    def run(self):
        self.fenPrincipal.mainloop()

TkinterVue2().run()