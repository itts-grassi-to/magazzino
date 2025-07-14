import tkinter as tk
class Categoria:
    def __init__(self,ini):
        self.root = tk.Toplevel()
        self.root.title(ini["titolo"])
        self.root.geometry(ini["dimensioni"])
        self.root.resizable(False, False)
        self.root.grid()
        self.root.attributes("-topmost",1) 
class VisuCategoria(Categoria):
    def __init__(self):
        w="400"
        h="300"
        ini = {"id":"Visualizza","titolo":"Visualizza categoria","dimensioni":w+"x"+h}
        super().__init__(ini)
    def getSelezionato(self):
        ival=1
        sval="computer"
        return ival,sval