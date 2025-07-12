import tkinter as tk
class Prodotto:
    def __init__(self,ini):
        self._root = tk.Tk()
        self._root.title(ini["titolo"])
        self._root.geometry(ini["dimensioni"])
        self._root.resizable(False, False)
        self._root.grid()

class ProdottoNuovo(Prodotto):
    def __init__(self):
        w="400"
        h="300"
        ini = {"id":"NUOVO","titolo":"Nuovo prodotto","dimensioni":w+"x"+h}
        super().__init__(ini)
        self.__fr1 =tk.Frame(self._root,width=int(w),height=int(h)/2)
        self.__fr1.grid(column=0,row=0,padx=5,pady=5,sticky="NSEW")

        self._root.mainloop()

class ProdottoModifica(Prodotto):
    def __init__(self):
        pass

p=ProdottoNuovo()

